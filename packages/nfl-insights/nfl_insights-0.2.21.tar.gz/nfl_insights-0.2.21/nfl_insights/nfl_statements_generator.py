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
        # get ostats from external caller or initialize it.
        self._ostats = ostats
        if ostats is None:
            self._ostats = NFLTeamAnalytics([season])
        # read the definition JSON.
        #oldtemplateDefFilename = '{}/statement_templates.json'.format(Path(__file__).parent)
        templateDefFilename = '{}/statement_templates_new.json'.format(Path(__file__).parent)
        self.language = ProUtils.get_dict_from_jsonfile(templateDefFilename)
        #self._refactor_definition_json(self.language)
        #ProUtils.save_dict_to_jsonfile(newtemplateDefFilename, self.language)
        self.statementsDF = pd.DataFrame(columns=['Interest', 'teamName', 'dimensions', 'statObject', 'statName', 'statValue', 'absFactor', 'rank', 'nItems', 'calculation', 'Sentiment', 'Text', 'Template'])
        self.stats = self._ostats.get_stats(teamType='offense')
        for key1, _statDict in self._ostats.allStatsDict.items():
            _season, _statname, _object = key1
            logger.info('Covering main key: %s', key1)
            for key2, statTable in _statDict.items():
                _dims, _calculation = key2
                _dimensions = eval(_dims)
                _statementFunc = getattr(self, '_do_' + _calculation)
                _statementsDF = _statementFunc(statTable, _statname, _object, _dimensions, _calculation)
                self.statementsDF = self.statementsDF.append(_statementsDF)

    @contendo_classfunction_logger
    def _refactor_definition_json(self, defJson):
        _statDefs = self._ostats.statsDict
        # updating the stats statements per team.
        _statements = defJson['entities']['statnames']
        for _statname, _statStatements in _statements.items():
            _statDef = _statDefs[_statname]
            _statTeams = _statDef['TeamObjects'].split(',')
            _newStatDef = dict()
            for _teamType, _teamSentences in _statStatements.items():
                _newTeamDef = dict()
                _tt = _teamType.replace('Team', '')
                if _tt in _statTeams:
                    _newTeamDef['isRelevant'] = True
                    if _tt in _statDef['Direction'].split(','):
                        _newTeamDef['isReverse'] = False
                    else:
                        _newTeamDef['isReverse'] = True
                else:
                    _newTeamDef['isRelevant'] = False
                    _newTeamDef['isReverse'] = False
                _newTeamDef['isPositive'] = not _newTeamDef['isReverse']
                _newTeamDef['sentences'] = _teamSentences
                _newStatDef[_teamType] = _newTeamDef
            _statements[_statname] = _newStatDef
        return

    @contendo_classfunction_logger
    def _get_statements_df(self, statTable, statName, object, dimensions, calculation):
        result = pd.DataFrame(columns=self.statementsDF.columns)
        if 'all' not in dimensions:
            return result
        distMeasure = self.get_dispersion(statTable, 10)
        if distMeasure < 0.15:
            numst = 1
        elif distMeasure < 0.3:
            numst = 3
        else:
            numst = 5
        rawStatements = self._get_statements(statTable, numst)
        if rawStatements.shape[0]>0:
            #logger.info(rawStatements.columns)
            result = rawStatements[self.statementsDF.columns]

        return result

    def _do_stat(self, statTable, statName, object, dimensions, calculation):
        return self._get_statements_df(statTable, statName, object, dimensions, calculation)

    def _do_ratio(self, statTable, statName, object, dimensions, calculation):
        return pd.DataFrame(columns=self.statementsDF.columns)

    def _do_pct(self, statTable, statName, object, dimensions, calculation):
        return pd.DataFrame(columns=self.statementsDF.columns)

    def _do_per_game(self, statTable, statName, object, dimensions, calculation):
        return pd.DataFrame(columns=self.statementsDF.columns)

    def _do_per_drive(self, statTable, statName, object, dimensions, calculation):
        return pd.DataFrame(columns=self.statementsDF.columns)

    def _do_per_play(self, statTable, statName, object, dimensions, calculation):
        return pd.DataFrame(columns=self.statementsDF.columns)

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
    def _get_statements(self, statTable, numst, thresh=1):
        # get interesting statements for a stat table - numst is number of top and bottom statements
        # result may be up to 2Xnumst statements
        # interest here is non contextual and based on standard deviation only
        _statements = pd.DataFrame()
        indices = list(statTable.index[0:numst])+list(statTable.index[len(statTable) - numst:len(statTable)])
        for ind in (indices):
            _statementRow = dict(statTable.loc[ind])
            _absFactor = abs(_statementRow['stdFactor'])-thresh
            if _absFactor > 0:
                _statementRow['Interest'] = min(1, _absFactor)
                _statementRow['absFactor'] = _absFactor
                self._update_statement_text(_statementRow)
                _statements = _statements.append(_statementRow, ignore_index=True)

        return _statements

    @contendo_classfunction_logger
    def _update_statement_text(self, statementRow: dict) -> None:

        _object = statementRow['statObject']
        _entity = statementRow['teamName']
        # calculate rank text
        _ranklist = self.language['entities']['ranks'][str(int(statementRow['rank']))]
        _ranktext = _ranklist[random.randint(0, len(_ranklist) - 1)]
        # get stat text
        _statdef = self.language['entities']['statnames'][statementRow['statName']][_object]
        _statsentences = _statdef['sentences']
        _stattext = _statsentences[random.randint(0, len(_statsentences) - 1)]
        _dimList = eval(statementRow['dimensions'])
        if all(x == 'all' for x in _dimList):
            _dimension = ""
            _dimpreposition = ""
        else:
            _dimIndex = int(not _dimList.index('all'))
            _dimension = self.language['entities']['dimensions'][_dimList[_dimIndex]]['text']
            _dimpreposition = self.language['entities']['dimensions'][_dimList[_dimIndex]]['prep']
        # get object description
        _objectDescriptions = self.language['entities']['objectDescriptions'][_object]
        _objectDescription = _objectDescriptions[random.randint(0, len(_objectDescriptions) - 1)]
        # get the template
        _sentiment = 'positive' if _statdef['isPositive'] else 'negative'
        _templates = self.language['templates'][_sentiment]
        _templateIndex = random.randint(0, len(_templates) - 1)
        _template = _templates[_templateIndex]['template']

        _statementText = _template.format(
            subject=_entity,
            rank=_ranktext,
            dimension=_dimension,
            dimprep=_dimpreposition,
            statname=_stattext,
            ObjectDescription=_objectDescription,
            X=int(statementRow['statValue'])
        )
        # remove blanks
        while _statementText.find('  ') > -1:
            _statementText = _statementText.replace('  ', ' ')

        #keep the text, template & sentiment
        statementRow['Text'] = _statementText
        statementRow['Sentiment'] = _sentiment
        statementRow['Template'] = _template

        return


@contendo_function_logger
def test():
    logger.info('Starting...')
    #os.chdir('{}/tmp/'.format(os.environ['HOME']))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{}/sportsight-tests.json'.format(os.environ['HOME'])
    nfls = NFLStatements(season='2019-regular')
    # saving the sentences & uploading to the cloud
    _nflSentencesFile = 'resource/nfl-sentences.csv'
    nfls.statementsDF.to_csv(_nflSentencesFile)
    #nfls._ostats.generator.nfldata.bqu.upload_file_to_gcp(bucketName=NFL_GCP_BUCKET, inFileName=_nflSentencesFile, targerFileName=_nflSentencesFile, timestamp=True)
    logger.info('Done')


if __name__ == '__main__':
    pd.set_option('display.max_columns', 1500)
    pd.set_option('display.width', 20000)
    contendo_logging_setup(default_level=logging.INFO)
    test()
