from datetime import datetime as dt
import json
import os
import pandas as pd
import logging
from typing import Optional

from setuptools.command.test import test

from contendo_utils import *
from nfl_insights import *

class NFLPbpContextBuilder:
    @contendo_classfunction_logger
    def __init__(self) -> None:
        self.ccm = ContendoConfigurationManager()
        self.dimentionsDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 71679784, 'ConditionCode')
        self.playPropMap = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 138336971, 'PropertyName')
        self.descriptionConfig = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 1063246855, 'Text')

    @contendo_classfunction_logger
    def reset(self, gameInfo: dict, season: str) -> None:
        self.playsList = list()
        self.playCounter = 0
        self.playIndex = 0
        self.gameInfo = gameInfo
        self._playContext = NFLPlayContext(gameInfo['awayTeam']['id'], gameInfo['homeTeam']['id'], year = season.split('-')[0])
        self.prevPlay = None
        self.inconsistentCount=0
        self.nofumbleInconsistentCount=0
        self.contextError = False
        self.homeDrive=0
        self.awayDrive=0
        self.teamDrive=0
        self.gameDrive=0
        self.awayScore = 0
        self.homeScore = 0

    @contendo_classfunction_logger
    def add_next_play(self, play: dict) -> dict:
        _newplay = self._create_play(play)
        # TODO: Handle penalties and subplays

        # finally set the previous play
        self.prevPlay = _newplay

        # handle subplays if exists
        _newplay['nFumbles'] = 0
        self.subplayIndex = 0
        subplays = play[_newplay['playType']].get('subPlays', list())
        if subplays:
            for subPlay in subplays:
                found = False
                for sybplayName in ['fumble', 'lateralPass', 'pass', 'rush']:
                    if sybplayName in subPlay:
                        found = True
                        if type(subPlay[sybplayName]) == dict:
                            subplays2 = [subPlay[sybplayName]]
                        elif type(subPlay[sybplayName]) == list:
                            subplays2 = subPlay[sybplayName]
                        else:
                            logger.error('Error: illegal Subplay: %s', subPlay)
                        for subplay2 in subplays2:
                            self._create_subplay(_newplay, {sybplayName: subplay2}, parent=play)
                if not found:
                    logger.error('Error: Unknown Subplay: %s', subPlay)

        # handle penalties.
        penalties = play[_newplay['playType']].get('penalties', list())
        if penalties:
            for penalty in penalties:
                if type(penalty['penalty']) == dict:
                    penalties2 = [penalty['penalty']]
                else:
                    penalties2 = penalty['penalty']

                for penalty2 in penalties2:
                    self._create_subplay(_newplay, {'penalty': penalty2}, parent=play)

        if 'inconsistent' in _newplay and _newplay['nFumbles'] == 0:
            self.nofumbleInconsistentCount += 1

        return _newplay

    @contendo_classfunction_logger
    def _create_play(self, play, parent=None, playStatus=None):
        try:
            _newplay = dict()
            _isSubplay = (parent is not None)
            #
            # processing play keys
            for key, value in play.items():
                if key == 'description':
                    _newplay['playDescription'] = value
                elif key == 'playStatus':
                    self._digest_playstatus(_newplay, value)
                elif key in ['pass', 'rush', 'sack', 'kick', 'penalty', 'punt', 'fumble', 'fieldGoalAttempt',
                             'extraPointAttempt', 'lateralPass']:
                    _newplay['playType'] = key
                    self._digest_play_properties(_newplay, playType=key, playProperties=value)
                    if key == 'penalty' and not parent:
                        properties = value.get('penalty')
                        self._digest_play_properties(_newplay, playType='penalty', playProperties=properties)
                    # set team_id to team in possession
                else:
                    _newplay[key] = value

            if not 'playType' in _newplay:
                logger.error('Error play: \n%s\n_newplay:\n%d.%s\n', play, self.playCounter+1, _newplay)
                return None

            #
            # Processing post-play info (if top play)
            if not _isSubplay: # main play
                #
                # getting initial home and away scores.
                _newplay['awayScore'] = self.awayScore
                _newplay['homeScore'] = self.homeScore

                self._digest_description(_newplay)
                try:
                    consistent = self._playContext.play(playjson=play)
                except Exception as e:
                    logger.exception('Error GC-processing play:\n%s\n', play)
                    self.contextError = True
                    self.playCounter += 1
                    _newplay['index'] = self.playCounter
                    return _newplay

                if not consistent and self.prevPlay:
                    try:
                        errors = '\n\t Inconsistent:'
                        if self.prevPlay["lineOfScrimmage"]:
                            if self.prevPlay["lineOfScrimmage_team_id"]!=self._playContext.ballTerritory and self._playContext.ballPosition != 50 and self._playContext.ballTerritory != -1:
                                errors += 'lineOfScrimmage team territory, '
                            if int(self.prevPlay["lineOfScrimmage_yardLine"]) != self._playContext.ballPosition:
                                errors += 'lineOfScrimmage yardLine, '
                            if int(self.prevPlay["currentDown"]) != self._playContext.down:
                                errors += 'currentDown, '
                            if int(self.prevPlay["yardsRemaining"]) != self._playContext.yardsRemaining:
                                errors += 'yardsRemaining, '
                        if int(self.prevPlay["teamInPossession_id"]) != self._playContext.offense:
                            errors += 'teamInPossession, '
                        logger.debug('Inconsistent playstatus: %d. %s, Errors:%s', self.playCounter, self.prevPlay['playDescription'], errors)
                        self.inconsistentCount += 1
                        _newplay['inconsistent'] = True
                    except Exception as e:
                        logger.Error('Error processing prev-play: %s\n', self.prevPlay)

                # Handle conversion
                if self._playContext.conversion:
                    _newplay['isConversion'] = True
                else:
                    _newplay['isConversion'] = False

                # handling interception and touchdown
                if self._playContext.intercepted:
                    _newplay['isIntercepted'] = True

                # handle Drives
                if self._playContext.drive>0 and self._playContext.drive > self.gameDrive:
                    self.gameDrive = self._playContext.drive
                    if _newplay['teamInPossession_id']==self._playContext.homeTeam:
                        self.homeDrive += 1
                        self.teamDrive = self.homeDrive
                    else:
                        self.awayDrive += 1
                        self.teamDrive = self.awayDrive

            else: # not top - subplay
                self._digest_playstatus(_newplay, playStatus)
                _newplay['playDescription'] = parent['playDescription']
                _newplay['awayScore'] = parent['awayScore']
                _newplay['homeScore'] = parent['homeScore']


            # setting the kicking team for extraPointAttempt
            if _newplay['playType'] in ['extraPointAttempt', 'fieldGoalAttempt']:
                _newplay['kickingTeam_id'] = _newplay['teamInPossession_id']

            # offense/defense/kicking/return team setting
            if not 'team_id' in _newplay:
                if 'kickingTeam_id' in _newplay:
                    _newplay['team_id'] = _newplay['kickingTeam_id']
                elif 'recoveringTeam_id' in _newplay:
                    _newplay['team_id'] = _newplay['recoveringTeam_id']
                else:
                    _newplay['team_id'] = _newplay['teamInPossession_id']

            _newplay['offenseTeam_id'] = _newplay['teamInPossession_id']
            _newplay['defenseTeam_id'] = self._playContext.awayTeam if _newplay['offenseTeam_id'] == self._playContext.homeTeam else self._playContext.homeTeam
            if 'kickingTeam_id' in _newplay:
                _newplay['returnTeam_id'] = self._playContext.awayTeam if _newplay['kickingTeam_id'] == self._playContext.homeTeam else self._playContext.homeTeam

            # handle scorediff
            _newplay['scoreDiff'] = abs(_newplay['homeScore'] - _newplay['awayScore'])
            if _newplay['teamInPossession_id'] == self._playContext.homeTeam:
                _newplay['teamScoreDiff'] = _newplay['homeScore'] - _newplay['awayScore']
            else:
                _newplay['teamScoreDiff'] = _newplay['awayScore'] - _newplay['homeScore']

            # Handle touchdown
            if _newplay.get('isTouchdown', False): # TD after punt or kick
                _newplay['returnTouchdown'] = True

            if _newplay.get('isEndedWithTouchdown', False):
                if _isSubplay:
                    if _newplay['team_id'] == parent['team_id']:
                        _newplay['offenseTouchdown'] = True
                    else:
                        _newplay['defenseTouchdown'] = True
                else:
                    if self._playContext.intercepted:
                        _newplay['defenseTouchdown'] = True
                    else:
                        _newplay['offenseTouchdown'] = True

            # play (and subplays) been canceled.
            _newplay['isCanceled'] = self._playContext.isCanceled
            if _newplay['playType'] == 'punt':
                _newplay['netYards'] = _newplay.get('yardsKicked',0) - _newplay.get('yardsReturned',0)

            # handling score update
            self._calculate_points(_newplay)

            # handling drive
            _newplay['gameDrive'] = self._playContext.drive
            if self.gameDrive > 0:
                _newplay['teamDrive'] = self.teamDrive
                _newplay['uniqueTeamDrive'] = '{}-{}-{}'.format(self.gameInfo['id'], _newplay['team_id'], self.teamDrive)
            else:
                _newplay['teamDrive'] = 0

            # handling play-counter
            self.playCounter += 1
            if not _isSubplay:
                self.playIndex += 1
            else:
                self.subplayIndex+=1
                _newplay['subplayIndex'] = self.subplayIndex

            _newplay['index'] = self.playCounter
            _newplay['playIndex'] = self.playIndex
            _newplay['uniquePlayIndex'] = '{}-{}-{}'.format(self.gameInfo['id'], _newplay['team_id'], self.playIndex)
            #_newplay['context'] = self.get_play_context_dimentions(_newplay)

            self.playsList.append(_newplay)
        except Exception as e:
            logger.error('Error processing play:\n%s\nNewplay: %s\n', play, _newplay)
            raise e

        return _newplay

    @contendo_classfunction_logger
    def _create_subplay(self, newplay, subplay, parent):
        _newsubplay = self._create_play(subplay, parent=newplay, playStatus=parent['playStatus'])
        _newsubplay['parentIndex'] = newplay['index']
        _newsubplay['parentPlayType'] = newplay['playType']
        _newsubplay['isSubplay'] = True
        if _newsubplay['playType'] == 'fumble':
            newplay['nFumbles'] += 1

    @contendo_classfunction_logger
    def _calculate_points(self, newplay):
        # Touchdown
        if 'offenseTouchdown' in newplay:
            if newplay.get('isTwoPointConversion', False):
                newplay['offensePoints'] = 2 # TwoPointsConversion
            else:
                newplay['offensePoints'] = 6 # Offensive TD
        elif 'defenseTouchdown' in newplay:
            newplay['defensePoints'] = 6
        elif 'returnTouchdown' in newplay:
            newplay['returnPoints'] = 6
        # fieldGoalAttempt
        elif newplay['playType'] == 'fieldGoalAttempt' and newplay.get('isGood', False):
            newplay['kickingPoints'] = 3
        # extraPointAttempt
        elif newplay['playType'] == 'extraPointAttempt' and newplay.get('isGood', False):
            newplay['kickingPoints'] = 1
        # saftey
        elif newplay.get('isSafety', False) or newplay.get('isSafety1', False):
            newplay['defensePoints'] = 2
        else:
            pass
        
        for _key in ['defense', 'offense', 'kicking', 'return']:
            _pointsKey = _key+'Points'
            _teamKey = _key+'Team_id'
            if _pointsKey in newplay:
                _teamId = newplay[_teamKey]
                _points = newplay[_pointsKey]
                if _teamId == self._playContext.homeTeam:
                    self.homeScore+=_points
                else:
                    self.awayScore+=_points
                newplay['scoringPlay'] = self._playContext.scoringPlay
                newplay['pointsMade'] = _points



    @contendo_classfunction_logger
    def _digest_player(self, newplay, propname, player):
        if not player:
            return
        #newplay[propname+'_jerseyNumber'] = player['jerseyNumber']
        newplay[propname+'_position'] = player['position']
        #newplay[propname+'_lastName'] = player['lastName']
        #newplay[propname+'_firstName'] = player['firstName']
        newplay[propname+'_id'] = int(player['id'])

    @contendo_classfunction_logger
    def _digest_position(self, newplay, propname, position):
        if not position:
            return
        newplay[propname+'_point'] = position['point']
        newplay[propname+'_yardLine'] = int(position['yardLine'] if position['yardLine'] else -1)
        self._digest_team(newplay, propname+'_team', position['team'])

    @contendo_classfunction_logger
    def _digest_team(self, newplay, propname, team):
        if not team:
            return
        newplay[propname+'_id'] = int(team['id'])
        newplay[propname+'_abbreviation'] = team['abbreviation']

    @contendo_classfunction_logger
    def _digest_simple(self, newplay, propname, value):
        newplay[propname] = value

    @contendo_classfunction_logger
    def _digest_zout(self, newplay, propname, value):
        pass

    @contendo_classfunction_logger
    def _digest_lineofscrimmage(self, newplay, propname, lineofscrimmage):
        if not lineofscrimmage:
            newplay['lineOfScrimmage'] = False
            return
        else:
            newplay['lineOfScrimmage'] = True

        newplay[propname+'_yardLine'] = lineofscrimmage['yardLine']
        self._digest_team(newplay, propname+'_team', lineofscrimmage['team'])

    @contendo_classfunction_logger
    def _digest_description(self, play):
        if not 'playDescription' in play:
            return
        description = play['playDescription']
        playType = play['playType']

        for text, configDict in self.descriptionConfig.items():
            if configDict['playType'] == '' or configDict['playType'].find(playType) >-1:
                if description.find(text) > -1:
                    for i in range(1,3):
                        key = 'Key{}'.format(i)
                        if configDict[key] != '':
                            play[configDict[key]] = configDict['Value{}'.format(i)]

    @contendo_classfunction_logger
    def _digest_play_properties(self, newplay, playType, playProperties):
        for propname,value in playProperties.items():
            propDef = self.playPropMap[propname]
            # assert property is expected for this playtype
            if (propDef[playType] != 1):
                logger.error('Illegal property "{}" for playType "{}"'.format(propname, newplay['playType']))

            objType = propDef['ObjType']
            _digestFunc = self.__getattribute__('_digest_{objType}'.format(objType=str.lower(objType)))
            _digestFunc(newplay, propname, value)

    @contendo_classfunction_logger
    def _digest_playstatus(self, newplay: dict, playStatus: [dict,list]) -> None:
        if type(playStatus)==list:
            playStatus=playStatus[0]

        if type(playStatus) == dict:
            self._digest_play_properties(newplay, playType='playStatus', playProperties=playStatus)
        else:
            logger.error('Playstatus is not a dict, type: {}, {}'.format(type(playStatus), playStatus))

    @contendo_classfunction_logger
    def digest_pbp(self, pbpDict: dict, season) -> dict:
        self.reset(pbpDict['game'], season)
        #
        # process all newplays
        for play in pbpDict['plays']:
            self.add_next_play(play)

        return {'plays': self.playsList}

    @contendo_classfunction_logger
    def get_play_context_dimentions(self, play: dict, isDefense) -> dict:
        contextDims = dict()
        df = DictToObject(play)
        #
        # loop over all dimentions to check if the play is one of them
        for dim, dimDef in self.dimentionsDict.items():
            # get the condition
            if isDefense and len(dimDef['DefenseCondition'])>0:
                condition = dimDef['DefenseCondition']
                logger.debug('Defense condition %s', dim)
            else:
                condition = dimDef['Condition']

            # add playtype to the condition test
            if dimDef['playType'] == 'all':
                dimentionQuery = condition
            else:
                dimentionQuery = '({}) & (df.playType=="{}")'.format(condition, dimDef['playType'])

            #logger.debug('Dim: %s, Condition: %s', dim, d)
            # execute the condition
            try:
                res = eval(dimentionQuery)
            except:
                res = 'N/A'

            contextDims[res] = contextDims.get(res, list())
            contextDims[res].append(dim)

        #logger.debug('Play dimensions:\nisDefense: %s\nDims: %s\nPlay:%s\n', isDefense, contextDims, play)
        return contextDims

# Main Test function
@contendo_function_logger
def test():
    startTime=dt.now()
    pd.set_option('display.max_columns', 200)
    pd.set_option('display.width', 2000)
    #os.environ['CONTENDO_AT_HOME'] = 'y'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.environ['CONTENDO_DEV']='y'
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))

    testfile = 'game_playbyplay-2019-regular-51555-20192010-CIN-JAX.json'
    testfile = 'game_playbyplay-2019-regular-51578-20192710-NE-CLE.json'
    pbpDict = ProUtils.get_dict_from_jsonfile('results/nfl/game_playbyplay/'+testfile)
    pcb = NFLPbpContextBuilder()
    newpbp = pcb.digest_pbp(pbpDict=pbpDict, season='2019-regular')
    #print(json.dumps(newpbp))
    ProUtils.save_dict_to_jsonfile(testfile, newpbp)

    df = pd.DataFrame(newpbp['plays'])
    print(df.shape, df.columns)
    df.to_csv(testfile+'.csv')

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.DEBUG)
    test()
