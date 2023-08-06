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
        _df = pd.read_csv('resource/nfl-sentences.csv')
        _df['Dims'] = _df.apply(lambda x: set(eval(x['Dimensions']))-{'all'}, axis=1)
        self._sentencesDF = _df

    def _get_sentences(self, context, threshold=0.5):
        dimset = set(context['dimensions'])
        self._sentencesDF['isin'] = self._sentencesDF.apply(lambda x: True if len(x['Dims'] & dimset) > 0 else False, axis=1)
        teams = str([context['hometeam'], context['awayteam']])
        _df = self._sentencesDF.query('isin & (Team in {}) & (Interest>{})'.format(teams, threshold))
        _df = _df.reset_index()[['Interest', 'Dims', 'Team', 'Text']]
        _df['Interest'] = _df['Interest'].round(3)
        _ret = list()
        for i, row in _df.iterrows():
            _sentence = dict(row)
            for key in _sentence:
                _sentence[key] = str(_sentence[key])
            _ret.append(_sentence)
        return _ret

    @contendo_classfunction_logger
    def add_next_play(self, play: dict) -> dict:
        return self._pbpContext.add_next_play(play)

    @contendo_classfunction_logger
    def get_context(self, sentences=True) -> dict:
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
        context['dimensions'] = set(self._pbpContext.get_play_context_dimentions(_lastPlay)[True])-{'all'}
        # get the sentences
        if sentences:
            _sentences = self._get_sentences(context)
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
        print_dict(context)

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
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    contendo_logging_setup(default_level=logging.INFO)
    test_sentences()
