SELECT
  schedule.id AS gameid,
  FORMAT('%s-%s-%s', FORMAT_TIMESTAMP('%Y%d%m', schedule.startTime), schedule.homeTeam.abbreviation, schedule.awayTeam.abbreviation) AS matchname,
  schedule.homeTeam.abbreviation AS homeTeamAbv,
  schedule.awayTeam.abbreviation AS awayTeamAbv,
  schedule.startTime,
  score.homeScoreTotal,
  score.awayScoreTotal,
  schedule.playedStatus,
  season
FROM
  `sportsight-tests.NFL_Data.seasonal_games`
LEFT JOIN
  UNNEST (Seasondata.games)
WHERE
  schedule.playedStatus = 'COMPLETED'
ORDER BY
  startTime DESC