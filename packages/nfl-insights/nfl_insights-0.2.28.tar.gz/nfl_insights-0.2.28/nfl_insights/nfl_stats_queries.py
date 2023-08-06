import os
import numpy as np
import pandas as pd
from datetime import datetime as dt
from pathlib import Path
import logging

import gspread

from contendo_utils import *
from nfl_insights import *

# noinspection PyUnresolvedReferences
class NFLStatsQueries():
    #
    # read in the configurations
    def __init__(self, project=None):
        #
        # get the initial configurations
        self.ccm = ContendoConfigurationManager()
        self.sourcesConfigDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, NFL_DOMAIN_CONFIG_GID, 'Configname')
        self.statsDF = self.ccm.get_configuration_df(domain=NFL_DOMAIN_NAME, gid=530297342)
        self.statsDict = ProUtils.pandas_df_to_dict(self.statsDF, 'StatName')
        self.compStatsDF = self.ccm.get_configuration_df(NFL_DOMAIN_NAME, 1414140695)
        self.compStatsDict = ProUtils.pandas_df_to_dict(self.compStatsDF, 'StatName')
        self.dimentionsDF = self.ccm.get_configuration_df(NFL_DOMAIN_NAME, 71679784)
        self.dimentionsDict = ProUtils.pandas_df_to_dict(self.dimentionsDF, 'ConditionCode')
        self.dimentionsMatrixDict = self.ccm.get_configuration_dict(domain=NFL_DOMAIN_NAME, gid=779003421, key='GroupCode')
        self.ptmapDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 582380093, 'Object')
        #
        # initialize data
        #self.bqu = BigqueryUtils(project)
        self.nfldata = NFLGetData(project)
        #
        # cache variables
        self.pbpDF = None
        self.cachedDFs = dict()
        self.cachedSeasonDFs = dict()
        self.cachedTeams = dict()

    def _get_pbp_data(self, season=None):
        if self.pbpDF is None:
            self.pbpDF = self.nfldata.get_pbp_data()
            self.pbpDF['all']=1
            self.pbpDF['count']=1
            self.pbpDF['counter']=1
            self.pbpDF.set_index("season", inplace=True, append=True)
            self.pbpDF['yardsRushed'] = pd.to_numeric(self.pbpDF['yardsRushed'])

        _season = str(season)
        logger.debug(_season)
        if _season not in self.cachedSeasonDFs:
            if season: # len > 0 and not None...
                self.cachedSeasonDFs[_season] = self.pbpDF.query("season == '{}'".format(_season))
            else:
                self.cachedSeasonDFs[_season] = self.pbpDF

        return self.cachedSeasonDFs[_season]


    def _get_dimentions_condition(self, dimensions, object):
        retCond = 'True'
        isDefense = (object in ['defenseTeam', 'returnTeam'])
        for dim in dimensions:
            dimDef = self.dimentionsDict[dim]
            if isDefense and len(dimDef['DefenseCondition'])>0:
                condition = dimDef['DefenseCondition']
                logger.debug('Defense condition %s', dim)
            else:
                condition = dimDef['Condition']
            if condition and condition!='True':
                retCond += ' & ({})'.format(condition)

        return retCond

    def _get_stat_condition(self, statDef):
        condition = statDef['Condition']
        _function = statDef['Function']
        if condition:
            if condition=='True':
                pass
            elif _function == 'count':
                return '{}'.format(condition)
            else:
                return '({})'.format(condition, statDef['AggField'])

        return 'True'

    @contendo_classfunction_logger
    def _save_trace_df(self, traceDF, initialColumns, spreadId=None, sheetName=None):
        if not spreadId:
            spreadId = '1Q5O3ejSyEDZrlFXX04bOIWOqMxfiHJYimunZKtpFswU'
        if not sheetName:
            sheetName = 'trace'

        finalColumns=['season', 'gameid', 'gamename', 'homeScore', 'awayScore','quarter', 'playType', 'currentDown']

        for col in initialColumns:
            if col in traceDF.columns:
                finalColumns.append(col)

        for col in traceDF.columns:
            if col not in finalColumns:
                finalColumns.append(col)

        if 'CONTENDO_AT_HOME' in os.environ:
            from gspread_pandas import Spread, Client
            import google.auth
            credentials, project = google.auth.default()
            gc = gspread.Client(credentials)
            spread = Spread(spreadId, client=gc)
            spread.df_to_sheet(traceDF[finalColumns], index=False, sheet=sheetName, start='A1', replace=True)
            logger.info('trace can be found in this url: %s', spread.url)
        else:
            fileName = '{}.csv'.format(sheetName)
            traceDF[finalColumns].to_csv(fileName)
            logger.info ('Trace to file %s', fileName)
            try:
                import google.colab
                IN_COLAB = True
                from google.colab import files
                logger.debug ('Downloading %s', fileName)
                files.download(fileName)
            except Exception as e:
                logger.warning('Error getting trace file %s', fileName)
                IN_COLAB = False

    @contendo_classfunction_logger
    def get_team_counters(self, object, dimensions, season='2019-regular'):
        _dimensions=list()
        for _dim in dimensions:
            if self.dimentionsDict[_dim]['GroupCode'] == 'gamePeriod':
                _dimensions.append(_dim)
        _key = (object, str(_dimensions), season)
        if _key not in self.cachedTeams:
            _df = self._get_pbp_data(season)
            assert len(_dimensions) <= 1, 'Illegal dimensions, more than one game-period'+str(dimensions)
            if len(_dimensions) == 1:
                _query = '{}'.format(self._get_dimentions_condition(_dimensions, object)).replace('df.', '').replace('(True) &', '').replace('True &', '')
                logger.debug('Gameperiod filter query: %s', _query)
                _filteredDF = _df.query(_query)
            else:
                _filteredDF = _df
            _groupby = "['{object}_id']".format(object=object)
            _groupingeval = "_filteredDF.groupby({groupby}, as_index=False).agg({}'gameid': pd.Series.nunique, 'uniqueTeamDrive': pd.Series.nunique, 'uniquePlayIndex': pd.Series.nunique {}).sort_values(by='uniqueTeamDrive', ascending=False)"
            _groupingeval = _groupingeval.format('{', '}',groupby=_groupby)
            try:
                _teamsDF = eval(_groupingeval)
            except Exception as e:
                logger.exception("Error evaluating aggregation statemet: %s", _groupingeval)
                raise e
            _teamsDF.columns = ['teamId', 'nGames', 'nDrives', 'nPlays']
            _teamsDF.set_index('teamId', inplace=True)
            if object!='team':
                _mainDF = self.get_team_counters('team', ['all'], season).copy()
                for col in _teamsDF.columns:
                    _mainDF[col] = _teamsDF[col]
                _teamsDF = _mainDF
            else:
                _teamsDF['teamName'] = self.nfldata.get_teams_df(season)['teamFullname']

            self.cachedTeams[_key] = _teamsDF[['teamName', 'nGames', 'nDrives', 'nPlays']]

        return self.cachedTeams[_key]


    @contendo_classfunction_logger
    def pbp_get_stat(self, statName, object, dimensions=['all'], season='2019-regular', aggfunc=None, playType=None, filter='True', trace=False):
        assert type(season)==str, 'Season parameter must be string'
        assert statName in self.statsDict, "Illegal statName: '{}', must be one of {}".format(statName, self.statsDict.keys())
        assert object in self.ptmapDict, "Illegal object: '{}', must be one of {}".format(object, self.ptmapDict.keys())
        assert type(dimensions) == list, "Illegal dimensions argument {}, must be a list".format(dimensions)
        for _dim in dimensions:
            assert _dim in self.dimentionsDict, "Illegal statName: '{}', must be one of {}".format(_dim, self.dimentionsDict.keys())
        dimensions.sort()


        #
        # build the query conditions
        statDef = self.statsDict[statName]
        if object.replace('Team','') in statDef['Direction'].split(','):
            isAscending = False
        else:
            isAscending = True
        queryInst = {
            'statcond': self._get_stat_condition(statDef),
            'dimensionsCond': self._get_dimentions_condition(dimensions, object),
            'filtercond': filter,
            'isInplayCond': "(df.playType=='penalty') | (df.isCanceled != True)"
        }
        aggField = statDef['AggField']
        #
        # get the DF for the relevant season
        df = self._get_pbp_data(season)

        logger.debug('before aggfield processing %s', aggField)
        #df[aggField] = pd.to_numeric(df[aggField])
        #queryeval = 'df[({statcond}) & ({gamecond}) & ({playcond}) & ({filtercond}) & ({isInplayCond})]'.format(**queryInst)
        queryeval = 'df[({statcond}) & ({dimensionsCond}) & ({filtercond}) & ({isInplayCond})]'.format(**queryInst)
        _query = '({statcond}) & ({dimensionsCond}) & ({filtercond}) & ({isInplayCond})'.format(**queryInst).replace('df.', '').replace('(True) &', '').replace('True &', '')
        if queryeval in self.cachedDFs:
            filteredDF = self.cachedDFs[queryeval]
            logger.debug('From cache: Filtered DF shape: %s, Main DF shape: %s', filteredDF.shape, df.shape)
        else:
            try:
                logger.debug('before filtering: %s, %s', queryeval, _query)
                filteredDF = df.query(_query) # eval(queryeval)
                self.cachedDFs[queryeval] = filteredDF
                logger.debug('Filtered DF shape: %s, Main DF shape: %s', filteredDF.shape, df.shape)
            except Exception as e:
                logger.exception("Error evaluating filtering statemet: %s", queryeval)
                raise e

        #
        # return empty if no answers
        if filteredDF.shape[0]==0:
            logger.debug ('ZERO results for filter %s, total plays %s', queryeval, df.shape[0])
            return pd.DataFrame()

        objectDef = self.ptmapDict[object]
        statObject = objectDef['StatObject']
        if statObject=='team':
            groupby = "['{object}_id']"
            groupingeval = "filteredDF.groupby({groupby}, as_index=False).agg({}'{aggField}': '{aggFunc}', 'count': 'count' {})"
        else:
            groupby = "['{object}_id', '{object}_position', '{team}_id']"
            groupingeval = "filteredDF.groupby({groupby}, as_index=False).agg({}'{aggField}': '{aggFunc}', 'count': 'count', 'gameid': pd.Series.nunique, 'uniqueTeamDrive': pd.Series.nunique {})"
        groupby = groupby.format(object=object, team=objectDef['TeamType'])


        if not aggfunc:
            aggfunc = statDef['Function']
        logger.debug('before grouping')
        groupingeval = groupingeval.format('{', '}',groupby=groupby, aggField=aggField, aggFunc=aggfunc)

        try:
            finalDF = eval(groupingeval)
        except Exception as e:
            logger.exception("Error evaluating aggregation statemet: %s", groupingeval)
            raise e
        #
        # return empty if no answers
        _nItems = finalDF.shape[0]
        if _nItems==0:
            logger.debug ('ZERO results for aggregated table stat: %s, statobj: %s, dims: %s, total plays %s', statName, object, dimensions, _nItems)
            return pd.DataFrame()

        if trace:
            self._save_trace_df(filteredDF, finalDF.columns, sheetName='trace-{}-{}-{}'.format(statName, object, dimensions))

        if statObject=='team':
            finalDF.columns=['teamId', 'statValue', 'count']
            finalDF.set_index('teamId', inplace=True)
            teamsDF = self.get_team_counters(object, dimensions, season)
            finalDF = teamsDF.join(
                finalDF,
                #rsuffix='_dn',
                #on=_keys,
                how='left',
            )
            finalDF.fillna(0, inplace=True)
            #finalDF['teamName'] = teamsDF['teamFullname']
        else:
            finalDF.columns=['playerId', 'position', 'teamId', 'statValue', 'count', 'nGames', 'nDrives']
            finalDF.set_index(['playerId', 'teamId'], inplace=True)
            #playersDF = self.nfldata.get_players_df(season=season)
            #print(finalDF)
            #print(playersDF)
            #finalDF['firstName'] = playersDF['firstName']
            #finalDF['lastName'] = playersDF['lastName']

        #cols = finalDF.columns.copy()
        # if teamId:
        #     finalDF = finalDF[teamId]
        #     if finalDF.shape[0] == 0:
        #         record=dict()
        #         for col in finalDF.columns:
        #             record[col] = None
        #         record['teamId'] = teamId
        #         record['statValue'] = 0
        #         record['count'] = 0
        #         record['rank'] = -1
        #         finalDF = pd.DataFrame([record])
        # if playerId:
        #     playerDict = self.nfldata.get_player_by_id(playerId)
        #     finalDF = finalDF[playerDict['playerId'], playerDict['teamId']]
        #     if finalDF.shape[0] == 0:
        #         record = dict()
        #         for col in finalDF.columns:
        #             record[col] = None
        #         record['playerId'] = playerId
        #         record['firstName'] = playerDict.get('firstName', '')
        #         record['lastName'] = playerDict.get('lastName', '')
        #         record['teamId'] = playerDict.get('teamId', 0)
        #         record['statValue'] = 0
        #         record['count'] = 0
        #         record['rank'] = -1
        #         finalDF = pd.DataFrame([record])
        #finalDF=finalDF[cols]
        # add the rank.
        #
        # return empty if no answers
        if finalDF.query('statValue!=0.0').shape[0]==0:
            logger.debug ('ZERO values for aggregated table stat: %s, statobj: %s, dims: %s, total plays %s', statName, object, dimensions, filteredDF.shape[0])
            return pd.DataFrame()
        finalDF.sort_values('statValue', ascending=isAscending, inplace=True)
        finalDF['nItems'] = min(_nItems, finalDF.shape[0])
        finalDF['rank'] = finalDF['statValue'].rank(method='min', ascending=isAscending)
        # add dimensional columns
        finalDF['statName'] = statName
        finalDF['statObject'] = object
        dimensions.sort()
        finalDF['dimensions'] = str(dimensions)
        finalDF['season'] = str(season)
        return finalDF

    @contendo_classfunction_logger
    def pbp_get_composed_stat(self, compstat, object, dimensions=['all'], season='2019-regular', filter='True'):
        assert compstat in self.compStatsDict, "Illegal statName: '{}', must be one of {}".format(compstat, self.compStatsDict.keys())
        compstatDef = self.compStatsDict[compstat]
        if object.replace('Team','') == compstatDef['Direction']:
            isAscending = False
        else:
            isAscending = True
        #
        # get the numerator data
        numerators = compstatDef['NumeratorStatNames'].replace(' ','').split(',')
        numeratorDF = pd.DataFrame()
        for numerator in numerators:
            _nattr = numerator.split(':')
            _numerator = _nattr[0]
            _object = object if len(_nattr)==1 else _nattr[1]
            print(_numerator, _object)
            if not _object:
                _object=object
            _df = self.pbp_get_stat(_numerator, object, dimensions, season, filter=filter)
            if _df.shape[0]==0:
                continue
            if numeratorDF.shape[0]==0:
                numeratorDF = _df.copy()
            else:
                for key in ['statValue', 'count']:
                    numeratorDF[key] += _df[key]
        if numeratorDF.shape[0]==0:
            return numeratorDF
        #
        # get the denominator data
        denominatorDF = pd.DataFrame()
        if compstatDef['DenominatorStatNames']!='':
            denominators = compstatDef['DenominatorStatNames'].replace(' ','').split(',')
            for denominator in denominators:
                _dattr = denominator.split(':')
                _denominator = _dattr[0]
                _object = object if len(_dattr)==1 else _dattr[1]
                print(_denominator, _object)
                _df = self.pbp_get_stat(_denominator, _object, dimensions, season, filter=filter)
                if _df.shape[0]==0:
                    continue
                if denominatorDF.shape[0]==0:
                    denominatorDF = _df.copy()
                else:
                    for key in ['statValue', 'count']:
                        denominatorDF[key] += _df[key]
        df = numeratorDF
        if denominatorDF.shape[0]>0:
            df['statValue'] = (df['statValue']/denominatorDF['statValue']*compstatDef['StatRatio']).fillna(0)
        df.sort_values(by='statValue', ascending=isAscending, inplace=True)
        df['rank'] = df['statValue'].rank(method='min', ascending=isAscending)
        #
        # updating the parameter-based columns
        df['statName'] = compstat
        df['statObject'] = object
        df['dimensions'] = str(dimensions)
        df['season'] = str(season)
        return df

    @contendo_classfunction_logger
    def get_stat_questions(self, statDF):
        import math
        logger.debug('Starting...')
        _fields = ['teamId', 'teamName', 'statValue', 'count', 'rank']
        _df1 = statDF.reset_index().query('statValue!=0')[_fields]
        _df1['rank'] = _df1['statValue'].rank(method='dense', ascending=False)
        _df1['on'] = 1
        _df1.set_index('on', inplace=True)
        _df1['statRange'] = _df1['statValue'].max() - _df1['statValue'].min()
        _df1['nRanks'] = _df1['rank'].nunique()
        #_df2 = _df1[['teamId', 'teamName', 'statValue', 'count', 'rank', 'nGames', 'nDrives', 'nPlays']]
        _df2 = _df1[_fields]
        _joinedDF = _df1.join(_df2, lsuffix='', rsuffix='2')
        _joinedDF = _joinedDF.query('rank<rank2').copy()
        if _joinedDF.shape[0]==0:
            return pd.DataFrame()
        _joinedDF.reset_index(inplace=True)
        _joinedDF['rankDiff'] = _joinedDF['rank2'] - _joinedDF['rank']
        _joinedDF['qScore'] =  _joinedDF.apply(
            lambda x: (1-math.fabs(x['statValue']-x['statValue2'])/x['statRange'])*100 +
                       (x['rank']/x['nRanks']*350 if x['rank']<x['nRanks']*0.2 else 70+x['rank']/x['nRanks']*30),
            axis=1
        )
        _joinedDF.sort_values('qScore', ascending=True, inplace=True)
        logger.debug('Done...')
        return _joinedDF

@contendo_function_logger
def test_all_stats(generator):
    counter=dict()
    results=[]
    for statName, statDef in generator.statsDict.items():
        if statDef['Condition']=='' or statDef['Doit'] != 'y':
            continue
        for condCode, condDef in generator.dimentionsDict.items():
            for object, objectDef in generator.ptmapDict.items():
                #
                # only do if defined as 1
                if statDef[object] != 'y':
                    continue

                #if condDef['Condition']=='' or playCondDef['Condition']=='':
                    #logger.debug ('skipping %s, %s, %s', statDef, condDef, playCondDef)
                    #continue
                if condDef['playType'] != 'all' and condDef['playType'].find(statDef['playType'])==-1:
                    continue

                df = generator.pbp_get_stat(statName=statName, object=object, dimensions=[condCode])
                isResults = (df.shape[0]>0)
                counter[isResults] = counter.get(isResults, 0)+1
                logger.info ('%s, %s, %s, %s, %s, %s', counter[isResults], isResults, df.shape, statName, object, condCode)
                if isResults:
                    results.append(
                        {
                            'StatName': statName,
                            'Object': object,
                            'StatObject': objectDef['StatObject'],
                            'dimensions': condCode,
                            'nResults': df.shape[0],
                        }
                    )

    print(counter)
    keys = results[0].keys()
    resultsDF = pd.DataFrame(results, columns=keys)
    from gspread_pandas import Spread, Client
    spread = Spread(generator.ccm.get_domain_docid('Football.NFL'))
    spread.df_to_sheet(resultsDF, index=False, sheet='PBP Stats results', start='A1', replace=True)

# Main Test function
@contendo_function_logger
def test():
    startTime=dt.now()
    pd.set_option('display.max_columns', 25)
    pd.set_option('display.width', 2000)
    #os.environ['CONTENDO_AT_HOME'] = 'y'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.environ['CONTENDO_DEV']='y'
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    generator = NFLStatsQueries()
    #print(generator._generate_pbp_query())
    # logger.info('Start querying data, delta = %s', dt.now() - startTime)
    # df = generator.get_team_counters('offenseTeam')
    # logger.info('Offense Teams Counters:\n%s', df)
    # df = generator.get_team_counters('defenseTeam')
    # logger.info('Defense Teams Counters:\n%s', df)
    # return

    df = generator.pbp_get_composed_stat('totalTD', 'offenseTeam', dimensions=['all', 'all'], season='2019-regular')
    #df = generator.pbp_get_stat(statName='completions', object='defenseTeam', dimensions=['leading', 'all'], season='2019-regular')
    #df = generator.get_stat_questions(df)
    logger.info('Columns={}, Shape={}\n\n{}\n\n'.format(df.columns, df.shape, df))
    return
    df = generator.pbp_get_stat(statName='fieldGoals', object='kickingTeam', dimensions=['all', 'all'], season='2019-regular')
    df1 = generator.pbp_get_stat(statName='fieldGoalsMade', object='kickingTeam', dimensions=['all', 'all'], season='2019-regular')
    df2 = generator.pbp_get_stat(statName='fieldGoalsMissed', object='kickingTeam', dimensions=['all', 'all'], season='2019-regular')
    #df = generator.pbp_get_stat(statName='extrapointBlocked', object='kickingTeam', dimensions=['all', 'all'], season='2019-regular')
    df['statValue'] = df['statValue']-df1['statValue']-df2['statValue']
    logger.info('Columns={}, Shape={}\n\n{}\n\n'.format(df.columns, df.shape, df))
    return
    df1 = generator.pbp_get_stat(statName='defensePoints', object='defenseTeam', dimensions=['all', 'all'], season='2019-regular')
    df2 = generator.pbp_get_stat(statName='kickingPoints', object='kickingTeam', dimensions=['all', 'all'], season='2019-regular')
    df3 = generator.pbp_get_stat(statName='returnPoints', object='returnTeam', dimensions=['all', 'all'], season='2019-regular')

    df['statValue']+= df1['statValue']
    df['statValue']+= df2['statValue']
    df['statValue']+= df3['statValue']
    df.sort_values('statValue', ascending=False, inplace=True)
    #df["statValue"] = df["statValue"].fillna(0)
    if df.shape[0]>0:
        a = np.array([float(i) / (sum(df["statValue"]) + 1e-10) for i in df["statValue"]])
        df['c1'] = a
        a = a ** 10
        df['c2'] = a
        zoDistribution = np.array([float(i) / (sum(a)) for i in a])
        df['zoDist'] = zoDistribution
        l2Norm = np.linalg.norm(zoDistribution, ord=2)
        df['l2Norm'] = l2Norm
        minUniformity = 1 / np.sqrt(len(zoDistribution))
        df['minUni'] = minUniformity
        distMeasure = (l2Norm - minUniformity) / (1 - minUniformity)
        df['dimMeasure'] = distMeasure
    logger.info('Columns={}, Shape={}\n\n{}\n\n'.format(df.columns, df.shape, df))
    return
    df1 = generator.pbp_get_stat(statName='fumbles', object='offenseTeam', dimensions=['all', 'all'], season='2019-regular')
    df2 = generator.pbp_get_stat(statName='rushTD', object='offenseTeam', dimensions=['all', 'all'], season='2019-regular')
    df = generator.pbp_get_stat(statName='passTD', object='offenseTeam', dimensions=['all', 'all'], season='2019-regular')
    df3 = generator.pbp_get_stat(statName='returnTD', object='defenseTeam', dimensions=['all', 'all'], season='2019-regular')
    df['statValue']+= df1['statValue']
    df['statValue']+= df2['statValue']
    df['statValue']+= df3['statValue']
    df.sort_values('statValue', ascending=False, inplace=True)
    logger.info('Columns={}, Shape={}\n\n{}\n\n'.format(df.columns, df.shape, df))
    return
    #df = generator.pbp_get_stat('rushes', 'rushingPlayer', ['conversion3', '4thQ'], season='2019-regular', trace=False, playerId=12606)
    df = generator.pbp_get_stat('rushes', 'rushingPlayer', ['conversion3', '4thQ'], season=['2019-regular'], trace=False)
    logger.info('Columns={}, Shape={}\n{}'.format(df.columns, df.shape, df))
    df = generator.pbp_get_composed_stat('passrushRatio', 'offenseTeam', season=['2019-regular'])
    df['teamName'] = generator.nfldata.get_teams_df('2019-regular')['teamFullname']
    logger.info('Columns={}, Shape={}\n{}'.format(df.columns, df.shape, df))
    logger.info('Done, delta=%s', dt.now() - startTime)

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.DEBUG)
    test()
