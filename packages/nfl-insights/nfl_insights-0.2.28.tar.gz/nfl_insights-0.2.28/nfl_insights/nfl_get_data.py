import os
import pandas as pd
from datetime import datetime as dt
from pathlib import Path
import logging

import gspread

from contendo_utils import *
from nfl_insights import *

# noinspection PyUnresolvedReferences
class NFLGetData():
    #
    # read in the configurations
    def __init__(self, project=None):
        #
        # get the initial configurations
        self.ccm = ContendoConfigurationManager()
        #
        # initialize BQ
        self.bqu = BigqueryUtils(project)
        #
        # data files definitions
        self.dataObjects = ['games', 'teams', 'players']
        self.resourceDir = 'resource'
        self.pbpDataFileName = '{}/nfl_pbp_data.csv'.format(self.resourceDir)
        #
        # data variables
        self.pbpDF = None
        self.gamesDF = None
        self.dataDFs = dict()

    @contendo_classfunction_logger
    def _update_nfl_data(self, source, outfile):
        assert source in self.dataObjects, 'Illegal source: {}, must be one of {}'.format(source, self.dataObjects)
        _query = ProUtils.get_string_from_file('{}/queries/nfl_{}_info.sql'.format(Path(__file__).parent, source))
        _df = self.bqu.execute_query_to_df(_query)
        logger.debug('Read %s query data, shape=%s, columns=%s', source, _df.shape, _df.columns)
        ProUtils.create_path_directories(outfile)
        _df.to_csv(outfile, index=False)
        url = self.bqu.upload_file_to_gcp(NFL_GCP_BUCKET, outfile, outfile, timestamp=True)
        logger.debug('Updated %s file %s', source, outfile)
        self.dataDFs[source]=_df

    @contendo_classfunction_logger
    def _read_nfl_data(self, source, update=False):
        #
        # Read the pbp data from file.
        _datafile = '{resourceDir}/{source}_data.csv'.format(resourceDir=self.resourceDir, source=source)
        if update:
            logger.debug('Updating %s data', source)
            self._update_nfl_data(source, _datafile)

        # getting the source DF is required (first time)
        if not source in self.dataDFs:
            self.bqu.download_from_gcp(NFL_GCP_BUCKET, _datafile, _datafile, checkTimestamp=True)
            self.dataDFs[source] = pd.read_csv(_datafile)

    @contendo_classfunction_logger
    def get_player_by_id(self, playerId, season='2019-regular'):
        self._read_nfl_data('players')
        query = '(playerId=={}) & (season=="{}")'.format(playerId, season)
        logger.debug('Players query= %s', query)
        _playerDF = self.dataDFs['players'].query(query)
        if _playerDF.shape[0] == 0:
            # Error
            logger.error('Player id %s not found', playerId)
            return {}

        return dict(_playerDF.iloc[0])

    @contendo_classfunction_logger
    def get_players_df(self, season):
        key=('players', season)
        if not key in self.dataDFs:
            self._read_nfl_data('players')
            _playersDF = self.dataDFs['players'].query('season=="{}"'.format(season))
            _playersDF.set_index(['playerId', 'teamId'], inplace=True)
            self.dataDFs[key] = _playersDF
        return self.dataDFs[key]

    @contendo_classfunction_logger
    def get_teams_df(self, season):
        key=('teams', season)
        if not key in self.dataDFs:
            self._read_nfl_data('teams')
            _teamsDF = self.dataDFs['teams'].query('season=="{}"'.format(season))
            _teamsDF.set_index(['teamId'], inplace=True)
            self.dataDFs[key] = _teamsDF
        return self.dataDFs[key]

    @contendo_classfunction_logger
    def get_games_df(self, season, update=True):
        key=('games', season)
        if not key in self.dataDFs:
            self._read_nfl_data('games', update)
            _gamesDF = self.dataDFs['games'].query('season=="{}"'.format(season))
            self.dataDFs[key] = _gamesDF
        return self.dataDFs[key]

    @contendo_classfunction_logger
    def _generate_pbp_query(self):
        exceptionList = [
            'interceptedAtPosition',
            'recoveringTeam', #abbreviation
            'fumblingTeam',
            'scrambles',
            'kneels',
        ]
        pbp_schema = self.bqu.get_table_schema(NFL_DATA_DATASET, NFL_PBP_TABLEID)
        fieldsList = []
        def aggregate_fieldslist(schema, parent=None):
            def calc_fieldname(name, parent):
                if parent:
                    return '{parent}.{name}'.format(parent=parent, **field)
                else:
                    return name

            for field in schema:
                name = field['name']
                if name in exceptionList or name[0]=='_':
                    continue

                fieldname = calc_fieldname(name, parent)
                if field['type'] == 'RECORD':
                    if field['mode'] == 'REPEATED':
                        logger.debug(name)
                        continue
                    else:
                        aggregate_fieldslist(field['fields'], fieldname)
                else:
                    fieldsList.append('{} as {}'.format(fieldname, fieldname.replace('.','_'), field['type']))

        aggregate_fieldslist(pbp_schema)
        fieldsStr = str(fieldsList).replace('[', '').replace(']', '').replace(',', ',\n').replace("'", '')
        query = 'SELECT {fields} FROM `sportsight-tests.NFL_Data.{tableId}`'.format(fields=fieldsStr, tableId=NFL_PBP_TABLEID)
        if 'CONTENDO_DEV' in os.environ:
            ProUtils.write_string_to_file('{}/queries/pbp_flat_query.sql'.format(str(Path(__file__).parent)), query)
        return query

    def get_pbp_data(self):
        #
        # Read the pbp data from file.
        if self.pbpDF is None:
            self.bqu.download_from_gcp(NFL_GCP_BUCKET, self.pbpDataFileName, self.pbpDataFileName, checkTimestamp=True)
            self.pbpDF = pd.read_csv(self.pbpDataFileName).fillna(0)

        return self.pbpDF

# Main Test function
@contendo_function_logger
def test():
    logger.info('Start...')
    startTime=dt.now()
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 200)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.environ['CONTENDO_DEV']='y'
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    nfldata = NFLGetData()
    print(nfldata.get_players_df(season='2019-regular'))
    print(nfldata.get_player_by_id(playerId=12606))
    print(nfldata.get_teams_df(season='2019-regular'))
    print(nfldata.get_games_df(season='2019-regular', update=True))
    logger.info('Done.')

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1500)
    pd.set_option('display.width', 20000)
    contendo_logging_setup(default_level=logging.DEBUG)
    test()
