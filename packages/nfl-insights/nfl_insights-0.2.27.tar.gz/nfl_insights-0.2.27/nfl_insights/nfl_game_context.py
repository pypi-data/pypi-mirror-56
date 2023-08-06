import os
import logging
import pandas as pd

from contendo_utils import *
from nfl_insights import *

class NFLGameContext:
    @contendo_classfunction_logger
    def __init__(self, gameInfo, season='2019-regular'):
        self._gameInfo = gameInfo
        self._pbpContext = NFLPbpContextBuilder()
        self._pbpContext.reset(gameInfo, season=season)
        self.nfldata = NFLGetData()
        self.teams = ProUtils.pandas_df_to_dict(self.nfldata.get_teams_df(season).reset_index(), 'teamId')
        self._load_sentences()

    def _load_sentences(self):
        # get the sentences file from GCP if required
        self.nfldata.bqu.download_from_gcp(NFL_GCP_BUCKET, NFL_SENTENCES_FILE, NFL_SENTENCES_FILE, checkTimestamp=True)
        _df = pd.read_csv(NFL_SENTENCES_FILE)
        _df['Dims'] = _df.apply(lambda x: set(eval(x['dimensions']))-{'all'}, axis=1)
        _df['Team'] = _df['teamName']
        self._sentencesDF = _df

    def _get_sentences(self, context, threshold=0.5):
        _filteredSentencesDF = pd.DataFrame()
        for teamPref in ['pos', 'def']:
            _dimset = set(context['{}Dimensions'.format(teamPref)])
            _teamName = context['{}TeamName'.format(teamPref)]
            _statObject = context['{}TeamType'.format(teamPref)]

            _df = self._sentencesDF.query('(teamName == "{}") & (statObject == "{}") & (Interest>{})'.format(_teamName, _statObject, threshold)).copy()
            _df['isin'] = _df.apply(lambda x: True if len(x['Dims'])==0 or len(x['Dims'] & _dimset) > 0 else False, axis=1)
            _df = _df.query('isin')
            _df['Interest'] = _df['Interest'].round(3)
            if _df.shape[0]>0:
                _filteredSentencesDF = _filteredSentencesDF.append(_df)

        _filteredSentencesDF.sort_values(by=['Interest', 'nItems', 'absFactor'], axis=0, inplace=True, ascending=False)
        _filteredSentencesDF = _filteredSentencesDF.reset_index()[['Interest', 'Dims', 'Team', 'Text', 'calculation']]
        _ret = list()
        for i, row in _filteredSentencesDF.iterrows():
            _sentence = dict(row)
            for key in _sentence:
                _type = type(_sentence[key])
                if _type in (set, list):
                    _value = ''
                    sep=''
                    for item in _sentence[key]:
                        _value+=sep+item
                        sep=','
                    _sentence[key] = _value
                else:
                    _sentence[key] = str(_sentence[key])
            _ret.append(_sentence)
        return _ret

    @contendo_classfunction_logger
    def add_next_play(self, play: dict) -> dict:
        return self._pbpContext.add_next_play(play)

    @contendo_classfunction_logger
    def get_context(self) -> dict:
        context = dict()
        _lastPlay = self._pbpContext.prevPlay
        context['description'] = _lastPlay['playDescription']
        context['awayteam'] = self.teams[self._pbpContext._playContext.awayTeam]['teamFullname']
        context['hometeam'] = self.teams[self._pbpContext._playContext.homeTeam]['teamFullname']
        context['score'] = self._pbpContext._playContext.score
        context['playtype'] = self._pbpContext._playContext.lastPlayType
        playkeys = ['quarter', 'currentDown', 'secondsElapsed', 'playIndex', '', '', '', '', '', '']
        for key in playkeys:
            if key in _lastPlay:
                context[key] = _lastPlay[key]
        # check status of the teams
        if 'returnTeam_id' in _lastPlay:
            context['posTeamId'] = _lastPlay['kickingTeam_id']
            context['posTeamType'] = 'kickingTeam'
            context['defTeamId'] = _lastPlay['returnTeam_id']
            context['defTeamType'] = 'returnTeam'
        else:
            context['posTeamId'] = _lastPlay['offenseTeam_id']
            context['posTeamType'] = 'offenseTeam'
            context['defTeamId'] = _lastPlay['defenseTeam_id']
            context['defTeamType'] = 'defenseTeam'
        # set the team names.
        if context['posTeamId']==self._pbpContext._playContext.awayTeam:
            context['posTeamName'] = context['awayteam']
            context['defTeamName'] = context['hometeam']
        else:
            context['defTeamName'] = context['awayteam']
            context['posTeamName'] = context['hometeam']
        # get the dimensions for each team
        context['posDimensions'] = set(self._pbpContext.get_play_context_dimentions(_lastPlay, isDefense=False)[True])
        context['defDimensions'] = set(self._pbpContext.get_play_context_dimentions(_lastPlay, isDefense=True)[True])
        # get the sentences
        _sentences = self._get_sentences(context)
        context['posDimensions'] = str(context['posDimensions'])
        context['defDimensions'] = str(context['defDimensions'])
        context['sentences'] = _sentences

        return context


@contendo_function_logger
def test():
    logger.info('Starting...')
    gamefile = 'game_playbyplay-2019-regular-51578-20192710-NE-CLE.json'
    pbpDict = ProUtils.get_dict_from_jsonfile('results/nfl/game_playbyplay/'+gamefile)
    gameInfo = pbpDict['game']
    plays = pbpDict['plays']
    gc = NFLGameContext(gameInfo)

    for play in plays:
        gc.add_next_play(play)
        context = gc.get_context()
        #logger.info(dict_to_string(context))
        logger.info(context['description'])

@contendo_function_logger
def test_sentences():
    gamefile = 'game_playbyplay-2019-regular-51578-20192710-NE-CLE.json'
    pbpDict = ProUtils.get_dict_from_jsonfile('results/nfl/game_playbyplay/'+gamefile)
    gameInfo = pbpDict['game']
    plays = pbpDict['plays']
    gc = NFLGameContext(gameInfo)
    gc.add_next_play(plays[0])
    context = gc.get_context()
    print(context)
    return
    import language_check
    #tool = language_check.LanguageTool('en-US')
    #matches = tool.correct('I love runing')
    from grammarbot import GrammarBotClient
    client = GrammarBotClient(api_key='KS9C5N3Y')
    res = client.check('I love running home')
    print(res)
    #return
    _count=0
    _sentenceList = gc._sentencesDF['Text']
    for _sentence in _sentenceList:
        _count+=1
        res = client.check(_sentence)
        if len(res.matches)>0:
            print(_count, _sentence, res)


if __name__ == '__main__':
    import os
    pd.set_option('display.max_columns', 25)
    pd.set_option('display.width', 2000)
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    contendo_logging_setup(default_level=logging.DEBUG)
    #test_sentences()
    test()
