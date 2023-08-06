import pandas as pd
import numpy as np
import random
import os
import json
from pathlib import Path
import logging

from contendo_utils import *
from nfl_insights import *

class NFLStatements:
    @contendo_classfunction_logger
    def __init__(self, season='2019-regular', ostats=None):
        # load the definition file
        self.templateDefFilename = '{}/statement_templates.json'.format(Path(__file__).parent)
        self.templateDefFilenameNew = '{}/statement_templates_new.json'.format(Path(__file__).parent)
        self.language = ProUtils.get_dict_from_jsonfile(self.templateDefFilename)
        # get ostats from external caller or initialize it.
        self._ostats = ostats
        if ostats is None:
            self._ostats = NFLTeamAnalytics([season])

    @contendo_classfunction_logger
    def _generate_all_statements(self, calculationsFilter=None, statsFilter=None):
        if not calculationsFilter:
            calculationsFilter=self.language['entities']['calculations'].keys()
        logger.debug('Generating all stats for calculation: %s', calculationsFilter)
        if not statsFilter:
            statsFilter=self._ostats.statsDict.keys()
        logger.debug('Generating all stats: %s', statsFilter)
        self._columns=['Interest', 'teamName', 'dimensions', 'statObject', 'statName', 'statValue', 'absFactor', 'rank', 'nItems', 'calculation', 'Sentiment', 'Text', 'Template', 'CompTemplate']
        outfile = open(NFL_SENTENCES_FILE, 'w')
        _writeHeaders = True
        self.statementsDF = pd.DataFrame(columns=self._columns)
        for key1, _statDict in self._ostats.allStatsDict.items():
            _season, _statname, _object = key1
            if not _statname in statsFilter:
                continue
            logger.debug('Covering main key: %s', key1)
            for key2, statTable in _statDict.items():
                _dims, _calculation = key2
                if not _calculation in calculationsFilter:
                    continue
                _dimensions = eval(_dims)
                _statementFunc = getattr(self, '_do_' + _calculation)
                _statementsDF = _statementFunc(statTable, _statname, _object, _dimensions, _calculation)
                #self.statementsDF = self.statementsDF.append(_statementsDF)
                # write to file
                if _statementsDF.shape[0]>0:
                    _statementsDF.to_csv(outfile, index=False, header=_writeHeaders)
                    # write header only in the first time
                    _writeHeaders=False
            #break
        outfile.close()
        self.statementsDF = pd.read_csv(NFL_SENTENCES_FILE)

    @contendo_classfunction_logger
    def _refactor_definition_json(self):
        _statDefs = self._ostats.statsDict
        # updating the stats statements per team.
        _statements = self.language['entities']['statnames']
        for _statname, _statDef in _statDefs.items():
            if _statDef['Doit'] !='y':
                continue
            _statTeams = _statDef['TeamObjects'].split(',')
            _statStatements = _statements.get(_statname, dict())
            _newStatDef = dict()
            for _teamType in ['offenseTeam', 'defenseTeam', 'kickingTeam', 'returnTeam']:
                _teamSentences = _statStatements.get(_teamType, dict())
                _newTeamDef = dict()
                _tt = _teamType.replace('Team', '')
                if _tt in _statTeams:
                    _newTeamDef['isRelevant'] = True
                    if _tt in _statDef['Direction'].split(',') and _tt not in _statDef['Sentiment'].split(','):
                        _newTeamDef['isPositive'] = True
                    else:
                        _newTeamDef['isPositive'] = False
                    _newTeamDef['sentences'] = _teamSentences.get('sentences', [_statDef['Description']])
                    _newTeamDef['format'] =  _statDef['Format']
                else:
                    _newTeamDef['isRelevant'] = False
                _newStatDef[_teamType] = _newTeamDef
            _statements[_statname] = _newStatDef

        # _calculations = self.language['entities']['calculations']
        # for _calc, _calcDef in _calculations.items():
        #     _newCalcDef = dict()
        #     _newCalcDef['texts'] = _calcDef
        #     if _calc == 'pct':
        #         _newCalcDef['format'] = '{:.0f}%'
        #     else:
        #         _newCalcDef['format'] = '{:.2f}'
        #     _calculations[_calc] = _newCalcDef
        #
        ProUtils.save_dict_to_jsonfile(self.templateDefFilenameNew, self.language)
        return

    def _do_stat(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    def _do_ratio(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    def _do_pct(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    def _do_per_game(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    def _do_per_drive(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    def _do_per_play(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    @contendo_classfunction_logger
    def _get_statements_df(self, statTable, statName, object, dimensions, calculation):
        result = pd.DataFrame(columns=self._columns)
        if 'all' not in dimensions:
            return result
        distMeasure = self.get_dispersion(statTable, 10)
        if distMeasure < 0.15:
            numst = 1
        elif distMeasure < 0.3:
            numst = 3
        else:
            numst = 5
        rawStatements = self._get_statements(statTable, dimensions, calculation, numst)
        if rawStatements.shape[0] > 0:
            # logger.info(rawStatements.columns)
            result = rawStatements[self._columns]

        return result

    @contendo_classfunction_logger
    def get_dispersion(self, statTable, factor):
        # find l2norm bsed measure of diversity
        statTable['statValue'] = statTable['statValue'].fillna(0)
        _arr = np.array(statTable['statValue'])
        a = _arr / sum(_arr)
        a = a ** factor
        zoDistribution = a / sum(a)
        l2Norm = np.linalg.norm(zoDistribution, ord=2)
        minUniformity = 1 / np.sqrt(len(zoDistribution))
        distMeasure = (l2Norm - minUniformity) / (1 - minUniformity)
        return distMeasure

    @contendo_classfunction_logger
    def _get_statements(self, statTable, dimensions, calculation, numst):
        # get interesting statements for a stat table - numst is number of top and bottom statements
        # result may be up to 2Xnumst statements
        # interest here is non contextual and based on standard deviation only
        _statements = pd.DataFrame()
        indices = list(statTable.index[0:numst])+list(statTable.index[len(statTable) - numst:len(statTable)])
        _interestThreshold = self.language['config']['interestThreshold']
        _valueThreshold = self.language['entities']['calculations'][calculation].get('valueThreshold', 0)
        for ind in (indices):
            _statementRow = dict(statTable.loc[ind])
            # skip if stat value is smallet than value-threshold (defined per-calculation).
            if abs(_statementRow['statValue'])<_valueThreshold:
                continue

            _absFactor = abs(_statementRow['stdFactor'])-_interestThreshold
            if _absFactor > 0:
                _statementRow['Interest'] = min(1, _absFactor)
                _statementRow['absFactor'] = _absFactor
                self._update_statement_text(_statementRow)
                _statementRow["Text"] += self._get_comparison_text(statTable, _statementRow)
                _statementRow["Text"] = _statementRow["Text"].replace(' .', '.')
                _statements = _statements.append(_statementRow, ignore_index=True)

        return _statements

    @contendo_classfunction_logger
    def _update_statement_text(self, statementRow: dict) -> None:

        # get stat text
        _statdef = self.language['entities']['statnames'][statementRow['statName']][statementRow['statObject']]
        _statsentences = _statdef['sentences']
        _stattext = _statsentences[random.randint(0, len(_statsentences) - 1)]
        # get the dimensions
        _dimList = eval(statementRow['dimensions'])
        if all(x == 'all' for x in _dimList):
            _dimension = ""
            _dimpreposition = ""
        else:
            _dimIndex = int(not _dimList.index('all'))
            _dimension = self.language['entities']['dimensions'][_dimList[_dimIndex]]['text']
            _dimpreposition = self.language['entities']['dimensions'][_dimList[_dimIndex]]['prep']
        # calculate rank text
        _ranklist = self.language['entities']['ranks'][str(int(statementRow['rank']))]
        _ranktext = _ranklist[random.randint(0, len(_ranklist) - 1)]
        # get object description
        _objectDescriptions = self.language['entities']['objectDescriptions'][statementRow['statObject']]
        _objectDescription = _objectDescriptions[random.randint(0, len(_objectDescriptions) - 1)]
        # get calculation description
        _calculationDef = self.language['entities']['calculations'][statementRow['calculation']]
        _calculationTexts = _calculationDef['texts']
        _calculation = _calculationTexts[random.randint(0, len(_calculationTexts) - 1)]
        # get the template
        if statementRow['calculation'] == 'pct':
            _sentiment = 'pct'
        else:
            _sentiment = 'positive' if _statdef['isPositive'] else 'negative'
        _templates = self.language['templates'][_sentiment]
        _templateIndex = random.randint(0, len(_templates) - 1)
        _template = _templates[_templateIndex]
        # format the value
        _valueFormat = _calculationDef.get('format', _statdef.get('format', '{:.f}'))
        _statFormatedValue = _valueFormat.format(float(statementRow['statValue']))

        _statementText = _template.format(
            subject=statementRow['teamName'],
            rank=_ranktext,
            dimension=_dimension,
            dimprep=_dimpreposition,
            statname=_stattext,
            ObjectDescription=_objectDescription,
            calculation=_calculation,
            X=_statFormatedValue
        )
        # remove double blanks
        while _statementText.find('  ') > -1:
            _statementText = _statementText.replace('  ', ' ')

        # keep the text, template & sentiment
        statementRow['Text'] = _statementText
        statementRow['Sentiment'] = _sentiment
        statementRow['Template'] = _template

        return

    @contendo_classfunction_logger
    def _get_comparison_text(self, statTable, statementRow):
        candidate = ""
        # default is compare to average
        avgdif = statementRow["avgDiff%"]
        stdfac = statementRow["avgDiff%"]
        thresh = 1 + abs(statementRow["avgDiff%"])
        if avgdif > 0:
            position = "higher"
            if avgdif > 100:
                diff = str(round((avgdif + 100) / 100, 1)) + " times"
            else:
                diff = str(round(avgdif, 1)) + "%"
        else:
            position = "lower"
            diff = str(round(abs(avgdif), 1)) + "%"
        candlist = self.language["entities"]['comparisons']["average"]
        candidateTemplate = candlist[random.randint(0, len(candlist) - 1)].format(diff=diff, position=position)
        candidate = candidateTemplate.format(diff=diff, position=position)
        # process the difference from the next team

        if avgdif < 0:
            position = "behind"
            comprank = statementRow["rank"] - 1
        else:
            position = "ahead of"
            comprank = statementRow["rank"] + 1
        if any(statTable["rank"] == comprank):
            comprow = statTable.loc[statTable["rank"] == comprank]
            facdif = abs(statementRow["stdFactor"]) - comprow["absStdFactor"]
            if facdif.iloc[0] / abs(statementRow["stdFactor"]) > 0.3:
                diff = str(round(
                    abs(statementRow["statValue"] - comprow["statValue"].iloc[0]) * 100 / comprow["statValue"].iloc[0],
                    1)) + "%"
                compentity = comprow["teamName"].iloc[0]
                comprank = str(int(comprow["rank"].iloc[0]))
                candlist = self.language["entities"]['comparisons']["next"]
                candidateTemplate = candlist[random.randint(0, len(candlist) - 1)]
                candidate = candidateTemplate.format(diff=diff, position=position, compentity=compentity,
                                                     comprank=comprank)

        statementRow['CompTemplate'] = candidateTemplate

        return candidate


@contendo_function_logger
def test():
    logger.info('Starting...')
    os.chdir('{}/tmp/'.format(os.environ['HOME']))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{}/sportsight-tests.json'.format(os.environ['HOME'])
    nfls = NFLStatements(season='2019-regular', ostats=None)
    #nfls._refactor_definition_json()
    nfls._generate_all_statements(calculationsFilter=['stat', 'ratio', 'pct', 'per_game', 'per_drive'], statsFilter=[])
    #nfls._generate_all_statements(calculationsFilter=['pct'], statsFilter=['offensePoints', 'fumbles', 'yardsRushed'])
    #nfls._generate_all_statements(calculationsFilter=['ratio'], statsFilter=[])
    # Sort the sentences
    nfls.statementsDF.sort_values(by=['Interest', 'nItems', 'absFactor'], axis=0, inplace=True, ascending=False)
    # saving the sentences
    nfls.statementsDF.to_csv(NFL_SENTENCES_FILE, index=False)
    # uploading the sentences - uncomment only when you want to upload them to the cloud and the demo.
    #nfls._ostats.generator.nfldata.bqu.upload_file_to_gcp(bucketName=NFL_GCP_BUCKET, inFileName=NFL_SENTENCES_FILE, targerFileName=NFL_SENTENCES_FILE, timestamp=True)
    logger.info('Done')


if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.DEBUG)
    pd.set_option('display.max_columns', 1500)
    pd.set_option('display.width', 20000)
    test()
