WITH
  teams AS (
  SELECT
    id AS teamId,
    season,
    FORMAT('%s %s',city, name) AS teamFullname
  FROM
    `sportsight-tests.NFL_Data.game_boxscore_*`
  LEFT JOIN
    UNNEST ( references.teamReferences )
  GROUP BY
    teamId,
    season,
    city,
    name ),
  games AS (
  SELECT
    schedule.id AS gameid,
    FORMAT('%s-%s-%s', FORMAT_TIMESTAMP('%Y%d%m', schedule.startTime), schedule.homeTeam.abbreviation, schedule.awayTeam.abbreviation) AS matchname,
    schedule.homeTeam.id AS homeTeamid,
    schedule.awayTeam.id AS awayTeamid,
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
    schedule.playedStatus = 'COMPLETED')
SELECT
  games.*,
  teams1.teamFullname as homeTeamName,
  teams2.teamFullname as awayTeamName
FROM
  games
  left join teams teams1 on teams1.teamId=games.homeTeamid and teams1.season=games.season
  left join teams teams2 on teams2.teamId=games.awayTeamid and teams2.season=games.season
ORDER BY
  startTime DESC