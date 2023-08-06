import pandas as pd
import numpy as np
import random
import os
import json
from pathlib import Path
import logging

from contendo_utils import *
from nfl_insights import NFLStatsQueries, NFLTeamAnalytics

class NFLStatements:
      def __init__(self, season = '2019-regular'):
         #need to init global self._so variable
         self._ostats = NFLTeamAnalytics([season])
         templateDefFilename = '{}/statement_templates.json'.format(Path(__file__).parent)
         self.language = ProUtils.get_dict_from_jsonfile(templateDefFilename)
         self.statementsDF = pd.DataFrame(columns = ['Interest', 'Team', 'Text', 'Dimensions', 'Object', 'Statname']) 
         self.stats = self._ostats.get_stats(teamType='offense')        
         for key in self._ostats.allStatsDict:
             for key1 in self._ostats.allStatsDict[key]:
                 statTable = self._ostats.allStatsDict[key][key1]
                 func = '_is_' + list(statTable['calculation'])[0].replace('-','_')                 
                 self.statementsDF = self.statementsDF.append(getattr(self, func)(statTable))
                 a = len(self.statementsDF)
         return
                 
      def _is_stat(self,statTable):
          result = pd.DataFrame(columns = ['Interest','Team','Text'])
          if 'all' not in eval(list(statTable['dimensions'])[0]): 
              return result
          distMeasure = self.get_dispersion(statTable,10)
          if distMeasure < 0.15:
             numst = 1
          elif distMeasure < 0.3:
             numst = 3
          else:
             numst = 5        
          rawStatements = self.get_raw_statements(statTable,numst)
          result = self.get_statement_texts(rawStatements,statTable,'stat_1d_')
          return result

      def _is_ratio(self,statTable):
          return
          
      def _is_pct(self,statTable):
          return
      
      def _is_per_game(self,statTable):
          return                         
          
      def _is_per_drive(self,statTable):
          return             

      def _is_per_play(self,statTable):
          return                         

      def get_dispersion(self,statTable, factor):
          # find l2norm bsed measure of diversity
          statTable['statValue'] = statTable['statValue'].fillna(0)
          _arr = np.array(statTable['statValue'])
          a = _arr/sum(_arr)
          a = a ** 10
          zoDistribution = a/sum(a)
          l2Norm = np.linalg.norm(zoDistribution, ord=2)
          minUniformity = 1 / np.sqrt(len(zoDistribution))
          distMeasure = (l2Norm - minUniformity) / (1 - minUniformity)          
          return distMeasure  
      
      def get_raw_statements(self, statTable, numst, thresh=1):
          # get interesting statements for a stat table - numst is number of top and bottom statements
          # result may be up to 2Xnumst statements
          #interest here is non contextual and based on standard deviation only
          statements = pd.DataFrame(columns = ['Interest','Team','Dimensions','Object','Statname']) 
          for ind in statTable.index[0:numst]:
              if statTable['stdFactor'][ind] > thresh:
                 interest = min(1,statTable['stdFactor'][ind]-thresh)
                 team = statTable['teamName'][ind]
                 dimensions = statTable['dimensions'][ind]
                 obj = statTable['statObject'][ind]
                 statname = statTable['statName'][ind]
                 statements = statements.append({'Interest':interest,'Team': team,'Object': obj, 'Statname': statname,'Dimensions': dimensions},ignore_index=True)
          for ind in statTable.index[len(statTable)-numst:len(statTable)]:
              if statTable['stdFactor'][ind] < -thresh:
                 interest = min(1,-statTable['stdFactor'][ind] - thresh)
                 team = statTable['teamName'][ind]
                 dimensions = statTable['dimensions'][ind]
                 obj = statTable['statObject'][ind]
                 statname = statTable['statName'][ind]
                 statements = statements.append({'Interest':interest,'Team': team, 'Object': obj, 'Statname': statname,'Dimensions': dimensions},ignore_index=True)
          return statements  
      
      def get_statement_texts(self,rawStatements,statTable,templistPrefix):          
          statements = rawStatements
          statements['Text'] = ""
          for ind in statements.index:
              stmt = statements.loc[ind] 
              statRow = statTable.loc[statTable['teamName'] == stmt['Team']]
              obj = statTable['statObject'].iloc[0]
              templist = templistPrefix+obj.replace('Team', '')
              templates = self.language['templates'][templist]
              temp_index = random.randint(0,len(templates)-1)
              tmplt = templates[temp_index]['template']
              subject = stmt['Team']
              ranklist = self.language['entities']['ranks'][str(int(statRow['rank'].values[0]))]
              rank = ranklist[random.randint(0,len(ranklist)-1)]
              statlist = self.language['entities']['statnames'][statRow['statName'].values[0]][obj]
              statname = statlist[random.randint(0,len(statlist)-1)]
              dimList = eval(statRow['dimensions'].values[0])
              if all(x == 'all' for x in dimList):
                 dimension = ""
                 dimprep = ""
              else:
                 dimIndex = int(not dimList.index('all'))
                 dimension = self.language['entities']['dimensions'][dimList[dimIndex]]['text'] 
                 dimprep = self.language['entities']['dimensions'][dimList[dimIndex]]['prep']

              statements.loc[statements['Team'] == stmt['Team'],'Text'] = tmplt.format(subject = subject,
                                                                   rank=rank,
                                                                   dimension=dimension,
                                                                   dimprep = dimprep,
                                                                   statname=statname,
                                                                   X=int(statRow['statValue'].values[0]))
          return statements

@contendo_function_logger
def test():
    logger.info('Starting...')
    os.chdir('{}/tmp/'.format(os.environ['HOME']))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{}/sportsight-tests.json'.format(os.environ['HOME'])
    nfls = NFLStatements(season = '2019-regular')
    nfls.statementsDF.to_csv('resource/nfl-sentences.csv')
    logger.info('Done')

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.INFO)
    test()
