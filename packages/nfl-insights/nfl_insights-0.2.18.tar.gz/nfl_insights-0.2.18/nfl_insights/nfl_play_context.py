import json


class NFLPlayContext:
    def __init__(self, awayteam, hometeam, year="2015"):

        ### recursion stack for penalties and subplays

        self.stack = []
        self.firstPlay = True
        ### meta data
        self._punt = self._kick  # punt and kick behave the same
        self.awayTeam = awayteam
        self.homeTeam = hometeam
        self.playTeams = [awayteam, hometeam]
        self.score = [0, 0]
        self.parentPlay = ""

        ### preplay variables
        self.preDown = 0
        self.prePosition = 0
        self.preTerritory = 0
        self.preOffense = 0
        self.preYardsRemaining = 0
        self.prescore = 0
        self.fdTargetTerritory = 0
        self.fdTargetyardLine = 0
        self.preQuarter = 0
        self.isCanceled = False
        self.consistent = False
        ### play variables
        self.lastPlayType = ""
        self.lastPlayRusher = 0
        self.lastPlayReturnMan = 0
        self.lastPlayReceiver = 0
        self.drive = 0
        self._drivenum = 0
        self.intercepted = False
        ### post play variables
        self.quarter = 1
        self.seconds = 0
        self.ballPosition = 35
        self.ballTerritory = -1
        self.down = 0
        self.yardsRemaining = 0
        self.offense = 0
        self.scoringPlay = False
        self.safetyScore = False
        self.conversion = 0
        # aux variables
        # defensive penalties that do not award automatic first down
        self.nfdPenalties = ["Encroachment",
                             "Neutral Zone Infraction",
                             "delay of game",
                             "illegal substitution",
                             "calling excess timeouts",
                             "running into a kicker",
                             "Defensive Offside"
                             ]
        # special team play types where penalties do not awad an auto first down
        self.stPlays = ["kick", "punt", "fieldGoalAttempt", "extraPointAttempt"]

        # special team play types where penalties do not award an auto first down
        self.nldPenalties = ["Illegal forward pass", "Intentional Grounding"]

        if int(year) < 2018:
            self.touchbackYardline = 20
        else:
            self.touchbackYardline = 25

    ### Process a play - return False if this play was not in line with the last play
    def play(self, playjson):

        self.isCanceled = False
        if "playStatus" in playjson.keys() and int(playjson["playStatus"]["quarter"]) == 3 and self.preQuarter == 2:
            self.firstPlay = True

        result = True
        self.consistent = True
        #
        # reset the points:
        self.offensePoints = 0
        self.defensePoints = 0
        self.kickingPoints = 0
        self.returnPoints = 0

        if "playStatus" in playjson.keys() and not self.firstPlay:
            result = self._checkConsistency(playjson)
            if result == False:
                self.consistent = False

        self.preYardsRemaining = self.yardsRemaining
        self.preOffense = self.offense
        self.prescore = self.score
        self.preQuarter = self.quarter
        self.preDown = self.down
        self.conversion = 0
        self.intercepted = False

        # Register and prepare the play
        self.lastPlay = playjson
        self.lastPlayType = list(set(list(playjson.keys())) - set(['description', 'playStatus']))[0]
        if "penalties" not in playjson[self.lastPlayType]:
            playjson[self.lastPlayType]["penalties"] = []
        if "subPlays" not in playjson[self.lastPlayType]:
            playjson[self.lastPlayType]["subPlays"] = []

            # Process play cancelling penalties
        if self._cancellingPenalty(playjson):
            return result
        # Save last variables to pre and fix any inconsistency with last play
        if "playStatus" in playjson.keys() and not self.firstPlay:
            self.quarter = int(playjson["playStatus"]["quarter"])
            self.seconds = int(playjson["playStatus"]["secondsElapsed"])
            self.offense = int(playjson["playStatus"]["teamInPossession"]["id"])
            if playjson["playStatus"]["currentDown"] is not None:
                self.preDown = int(playjson["playStatus"]["currentDown"])
                self.down = int(playjson["playStatus"]["currentDown"])
            else:
                self.preDown = 0
            if playjson["playStatus"]["lineOfScrimmage"] is not None:
                self.prePosition = int(playjson["playStatus"]["lineOfScrimmage"]["yardLine"])
                self.preTerritory = int(playjson["playStatus"]["lineOfScrimmage"]["team"]["id"])
                self.ballPosition = int(playjson["playStatus"]["lineOfScrimmage"]["yardLine"])
                self.ballTerritory = int(playjson["playStatus"]["lineOfScrimmage"]["team"]["id"])
                self.yardsRemaining = int(playjson["playStatus"]["yardsRemaining"])
                absScrimmage = self._absyardline(self.ballTerritory, self.ballPosition)
                absTarget = self._absyardline(self.fdTargetTerritory, self.fdTargetyardLine)
                dif = absTarget - absScrimmage - self.yardsRemaining
                if dif != 0:
                    absTarget -= dif
                    self.fdTargetTerritory, self.fdTargetyardLine = self._relyardline(absTarget)

        # Process the play according to its type
        func = "_" + self.lastPlayType
        getattr(self, func)(playjson)
        self.firstPlay = False

        # Process subplays (stack play and type for further processing)
        self.stack.append(self.lastPlay)
        self.stack.append(self.lastPlayType)
        self.stack.append(self.preOffense)
        self._processSubplays(playjson)
        self.preOffense = self.stack.pop()
        self.lastPlayType = self.stack.pop()
        self.lastPlay = self.stack.pop()

        # process post play penalties (stack play and type for further processing)
        self.stack.append(self.lastPlay)
        self.stack.append(self.lastPlayType)
        self._processPenalties(playjson)
        self.lastPlayType = self.stack.pop()
        self.lastPlay = self.stack.pop()

        # finalize remaining yards after all parts are processed
        self._computeYardsRemaining()

        self.scoringPlay = False
        self.safetyScore = False
        # process field scores
        self._processScores(playjson)

        if self.offense != self.preOffense and "playStatus" in playjson.keys():
            self._drivenum += 1
            self.drive = self._drivenum

        return result

    def _cancellingPenalty(self, playjson):
        # Process play cancelling penalties and return True if they exist
        self.preOffense = self.offense
        result = False
        if ("penalties" not in playjson[self.lastPlayType].keys() or len(
                playjson[self.lastPlayType]["penalties"]) == 0):
            return result
        for penalty in playjson[self.lastPlayType]["penalties"]:
            if type(penalty[
                        "penalty"]) is list:  # we got a list inside penalty - Oy Vey but only one should be enforced
                penalty = self._enforcedpenalty(penalty["penalty"])
                if not penalty:
                    break
            if penalty["penalty"]["isCancelsPlay"]:
                self.isCanceled = True
                territory, yardLine = self._advanceBall(penalty["penalty"]["yardsPenalized"],
                                                        penalty["penalty"]["enforcedAtPosition"]["yardLine"],
                                                        penalty["penalty"]["enforcedAtPosition"]["team"]["id"],
                                                        direction=penalty["penalty"]["team"]["id"], progress=0)
                self.ballPosition = yardLine
                self.ballTerritory = territory

                if int(penalty["penalty"]["team"]["id"]) != self.offense and \
                        penalty["penalty"]["description"] not in self.nfdPenalties \
                        and self.lastPlayType not in self.stPlays:
                    self._processFirstDown()
                if self.yardsRemaining > self.ballPosition and self.offense != self.ballTerritory:
                    self.yardsRemaining = self.ballPosition
                result = True
                self._processYardsAndDown(playjson)
        return result

    # process kicks and punts (NEED TO DEAL with successful on-side kicks)
    def _kick(self, playjson):
        self.drive = 0
        if playjson[self.lastPlayType]["isTouchback"]:
            self.ballTerritory = self.playTeams[
                int(not self.playTeams.index(playjson[self.lastPlayType]["kickingTeam"]["id"]))]
            if self.lastPlayType == "kick":
                self.ballPosition = self.touchbackYardline
            else:
                self.ballPosition = 20
            self.offense = self.playTeams[
                int(not self.playTeams.index(playjson[self.lastPlayType]["kickingTeam"]["id"]))]
        elif playjson[self.lastPlayType]["stoppedAtPosition"] is None and \
                playjson[self.lastPlayType]["retrievedAtPosition"] is not None:
            # Out of Bounds (Prbably)
            self.ballPosition = int(playjson[self.lastPlayType]["retrievedAtPosition"]["yardLine"])
            self.ballTerritory = int(playjson[self.lastPlayType]["retrievedAtPosition"]["team"]["id"])
            self.offense = self.playTeams[
                int(not self.playTeams.index(playjson[self.lastPlayType]["kickingTeam"]["id"]))]
        elif playjson[self.lastPlayType]["stoppedAtPosition"] is not None:
            self.ballPosition = int(playjson[self.lastPlayType]["stoppedAtPosition"]["yardLine"])
            self.ballTerritory = int(playjson[self.lastPlayType]["stoppedAtPosition"]["team"]["id"])
            self.offense = self.playTeams[
                int(not self.playTeams.index(playjson[self.lastPlayType]["kickingTeam"]["id"]))]
        self._processFirstDown()
        return

        # process a rush

    def _rush(self, playjson):
        self.drive = self._drivenum
        self.offense = playjson["rush"]["team"]["id"]
        if "playStatus" in playjson.keys():
            self.down = playjson["playStatus"]["currentDown"]
            self.yardsRemaining = int(playjson["playStatus"]["yardsRemaining"]) - int(playjson["rush"]["yardsRushed"])
        if len(self.stack) == 0: self.down += 1
        self.lastPlayRusher = playjson["rush"]["rushingPlayer"]["id"]
        if playjson["rush"]["stoppedAtPosition"] is not None:
            self.ballTerritory = int(playjson["rush"]["stoppedAtPosition"]["team"]["id"])
            self.ballPosition = int(playjson["rush"]["stoppedAtPosition"]["yardLine"])
        if len(playjson["rush"]["penalties"]) == 0:
            self._processYardsAndDown(playjson)
        if playjson["rush"]["isTwoPointConversion"]:
            self.down = 0
            self.yardsRemaining = 0
            self.ballPosition = 35
            self.ballTerritory = self.offense
        return

    # process a pass
    def _pass(self, playjson):
        self.drive = self._drivenum
        self.offense = playjson["pass"]["team"]["id"]
        if "playStatus" in playjson.keys():
            self.down = playjson["playStatus"]["currentDown"]
            self.yardsRemaining = int(playjson["playStatus"]["yardsRemaining"]) - int(
                playjson["pass"]["totalYardsGained"])
        if len(self.stack) == 0: self.down += 1
        if playjson["pass"]["isCompleted"]:
            self.lastPlayReceiver = playjson["pass"]["receivingPlayer"]["id"]
            if playjson["pass"]["stoppedAtPosition"] is not None:
                self.ballTerritory = int(playjson["pass"]["stoppedAtPosition"]["team"]["id"])
                self.ballPosition = int(playjson["pass"]["stoppedAtPosition"]["yardLine"])
        if playjson["pass"]["interceptedAtPosition"] is not None:
            self._processInterception(playjson)
        if len(playjson["pass"]["penalties"]) == 0:
            self._processYardsAndDown(playjson)
        if playjson["pass"]["isTwoPointConversion"]:
            self.down = 0
            self.yardsRemaining = 0
            self.ballPosition = 35
            self.ballTerritory = self.offense
        return

    # process a sack
    def _sack(self, playjson):
        self.drive = self._drivenum
        if "playStatus" in playjson.keys():
            self.yardsRemaining = int(playjson["playStatus"]["yardsRemaining"]) + int(playjson["sack"]["yardsLost"])
            self.down += 1
            self._processYardsAndDown(playjson)
            self.lastPlayRusher = playjson["sack"]["passingPlayer"]["id"]
            self.ballTerritory = int(playjson["sack"]["sackedAtPosition"]["team"]["id"])
            self.ballPosition = int(playjson["sack"]["sackedAtPosition"]["yardLine"])
        else:
            self.yardsRemaining -= playjson["sack"]["yardsLost"]
        return

    def _fumble(self, playjson):
        self.drive = self._drivenum
        if playjson["fumble"]["recoveringTeam"] is None or playjson["fumble"]["recoveringTeam"]["id"] == \
                playjson["fumble"]["fumblingTeam"]["id"]:
            netyards = playjson["fumble"]["yardsFumbled"] + playjson["fumble"]["yardsRecovered"]
            self.yardsRemaining = self.yardsRemaining - netyards
            self._processYardsAndDown(playjson)
        else:
            netyards = playjson["fumble"]["yardsFumbled"] - playjson["fumble"]["yardsRecovered"]
            self.offense = playjson["fumble"]["recoveringTeam"]["id"]
            self._processFirstDown()
        return

    def _lateralPass(self, playjson):
        self.drive = self._drivenum
        self.offense = playjson["lateralPass"]["team"]["id"]
        self.yardsRemaining = self.yardsRemaining - int(playjson["lateralPass"]["yardsGained"])
        if len(self.stack) == 0: self.down += 1
        self._processYardsAndDown(playjson)
        self.lastPlayReceiver = playjson["lateralPass"]["receivingPlayer"]["id"]
        if playjson["lateralPass"]["stoppedAtPosition"] is not None:
            self.ballTerritory = int(playjson["lateralPass"]["stoppedAtPosition"]["team"]["id"])
            self.ballPosition = int(playjson["lateralPass"]["stoppedAtPosition"]["yardLine"])
        return

    # process an extra point attempt
    def _extraPointAttempt(self, playjson):
        self.drive = 0
        self.scoringPlay = True
        self.down = 0
        self.yardsRemaining = 0
        self.ballPosition = 35
        self.ballTerritory = playjson["extraPointAttempt"]["team"]["id"]
        self.offense = int(playjson["extraPointAttempt"]["team"]["id"])
        if playjson["extraPointAttempt"]["isGood"]:
            self.score[self.playTeams.index(int(playjson["extraPointAttempt"]["team"]["id"]))] += 1
            self.kickingPoints = 1
        return

    # process an field goal attempt
    def _fieldGoalAttempt(self, playjson):
        self.drive = 0
        self.down += 1
        if playjson["fieldGoalAttempt"]["isGood"]:
            self.score[self.playTeams.index(int(playjson["fieldGoalAttempt"]["team"]["id"]))] += 3
            self.kickingPoints = 3
            self.down = 0
            self.ballPosition = 35
            self.ballTerritory = int(playjson["fieldGoalAttempt"]["team"]["id"])
            self.yardsRemaining = 0
            self.offense = int(playjson["fieldGoalAttempt"]["team"]["id"])
            self.lastPlayType = "fieldGoalAttempt"
            self.scoringPlay = True
        else:
            if self.down > 4:
                self.offense = self.playTeams[int(not self.playTeams.index(playjson["fieldGoalAttempt"]["team"]["id"]))]
                self.ballPosition = int(playjson["fieldGoalAttempt"]["kickedFromPosition"]["yardLine"])
                self.ballTerritory = int(playjson["fieldGoalAttempt"]["kickedFromPosition"]["team"]["id"])
                if self.ballPosition < 20:
                    self.ballPosition = 20
                self._processFirstDown()
        return

    # process penalty
    def _penalty(self, playjson):
        self.drive = 0
        penalty = playjson["penalty"]
        if penalty["penalty"]["enforcedAtPosition"] is None:
            penalty["penalty"]["enforcedAtPosition"] = playjson["playStatus"]["lineOfScrimmage"]
        territory, yardLine = self._advanceBall(penalty["penalty"]["yardsPenalized"],
                                                penalty["penalty"]["enforcedAtPosition"]["yardLine"],
                                                penalty["penalty"]["enforcedAtPosition"]["team"]["id"],
                                                direction=penalty["penalty"]["team"]["id"], progress=0)
        self.ballPosition = yardLine
        self.ballTerritory = territory
        if int(penalty["penalty"]["team"]["id"]) != self.offense and \
                penalty["penalty"]["description"] not in self.nfdPenalties \
                and self.lastPlayType not in self.stPlays:
            self._processFirstDown()
        if self.yardsRemaining > self.ballPosition and self.offense != self.ballTerritory:
            self.yardsRemaining = self.ballPosition
        return

    # get enforced penalty out of penalty list
    def _enforcedpenalty(self, penlist):
        for pen in penlist:
            if pen["enforcedAtPosition"] is not None:
                return dict({"penalty": pen})
        return False

    # regularize yardage remaining and down after a play
    def _processYardsAndDown(self, playjson):
        if self.yardsRemaining <= 0:
            self._processFirstDown()
        if self.down > 4:  # turnover on downs
            self.offense = self.playTeams[int(not self.playTeams.index(self.offense))]
            self._processFirstDown()

    # calculate ball position after penalty
    def _advanceBall(self, yardage, fromYard, fromTerritory, direction, progress=0):
        territory = fromTerritory
        if fromTerritory == direction:
            yardLine = fromYard - yardage
        else:
            yardLine = fromYard + yardage
        if yardLine > 50:
            yardLine = 100 - yardLine
            territory = self.playTeams[int(not self.playTeams.index(fromTerritory))]
        if direction == self.offense:
            self.yardsRemaining = self.preYardsRemaining + yardage
        else:
            self.yardsRemaining = self.preYardsRemaining - yardage
        if self.offense != self.preOffense:
            self.yardsRemaining = 10
        return territory, yardLine

    # reverse the posession in case of interception
    def _processInterception(self, playjson):
        self.intercepted = True
        self.offense = self.playTeams[int(not self.playTeams.index(playjson["pass"]["team"]["id"]))]
        if playjson["pass"]["stoppedAtPosition"] is not None:
            self.ballTerritory = int(playjson["pass"]["stoppedAtPosition"]["team"]["id"])
            self.ballPosition = int(playjson["pass"]["stoppedAtPosition"]["yardLine"])
        if self.ballPosition < 0:
            self.ballPosition = 20
        self._processFirstDown()

    # subplay recursion
    def _processSubplays(self, playjson):
        for subplay in reversed(playjson[self.lastPlayType]["subPlays"]):
            # Deal with vectors of fumbles or other subplays - UGLY feed bug
            for spn in ['fumble', 'lateralPass', 'pass', 'rush']:
                if spn in subplay:
                    if type(subplay[spn]) is list:
                        for p in subplay[spn]:
                            sp = {spn: p}
                            self.play(sp)
                    else:
                        self.play({spn: subplay[spn]})
        return

    # non play cancelling penalty loop
    def _processPenalties(self, playjson):
        if ("penalties" not in playjson[self.lastPlayType].keys() or len(
                playjson[self.lastPlayType]["penalties"]) == 0):
            return
        for penalty in reversed(playjson[self.lastPlayType]["penalties"]):
            if type(penalty[
                        "penalty"]) is list:  # we got a list inside penalty - Oy Vey but only one should be enforced
                penalty = self._enforcedpenalty(penalty["penalty"])
                if not penalty:
                    break
            if penalty["penalty"]["enforcedAtPosition"] is None:
                continue  # penalty is not enforced (declined)
            if not penalty["penalty"]["isCancelsPlay"]:
                progress = self._getProgress(playjson)
                territory, yardLine = self._advanceBall(penalty["penalty"]["yardsPenalized"],
                                                        penalty["penalty"]["enforcedAtPosition"]["yardLine"],
                                                        penalty["penalty"]["enforcedAtPosition"]["team"]["id"],
                                                        direction=penalty["penalty"]["team"]["id"], progress=progress)
                self.ballPosition = yardLine
                self.ballTerritory = territory
                # Deal with no loss of down
                if int(penalty["penalty"]["team"]["id"]) == self.offense and \
                        penalty["penalty"]["description"] not in self.nldPenalties \
                        and self.lastPlayType not in self.stPlays:
                    self.down = self.preDown
                    # deal with offensive pernalties accompanied by 1st down
                    absPosition = self._absyardline(territory, yardLine)
                    absScrimmage = self._absyardline(playjson["playStatus"]["lineOfScrimmage"]["team"]["id"],
                                                     playjson["playStatus"]["lineOfScrimmage"]["yardLine"])
                    if absPosition - absScrimmage > self.preYardsRemaining:
                        self._processFirstDown()
                if int(penalty["penalty"]["team"]["id"]) != self.offense and \
                        penalty["penalty"]["description"] not in self.nfdPenalties \
                        and self.lastPlayType not in self.stPlays:
                    self._processFirstDown()
        return

    # if goal to go adjust yards remaining
    def _ProcessGoalToGo(self):
        if self.yardsRemaining > self.ballPosition and self.offense != self.ballTerritory:
            self.yardsRemaining = self.ballPosition
        return

    # non play cancelling penalty loop
    def _processScores(self, playjson):
        if playjson[self.lastPlayType].get("isEndedWithTouchdown", False) and not playjson[self.lastPlayType].get(
                "isTwoPointConversion", False):
            self.score[self.playTeams.index(self.offense)] += 6
            if self.offense == self.preOffense:
                self.offensePoints = 6
            else:
                if self.lastPlayType in self.stPlays:
                    self.returnPoints = 6
                else:
                    self.defensePoints = 6

            self.down = 0
            self.yardsRemaining = 0
            self.ballPosition = 2
        if playjson[self.lastPlayType].get("isTwoPointConversion", False) and playjson[self.lastPlayType].get(
                "isEndedWithTouchdown", False):
            self.score[self.playTeams.index(self.offense)] += 2
            self.offensePoints = 2
            self.down = 0
            self.yardsRemaining = 0
            self.ballPosition = 35
            self.ballTerritory = self.offense
        if playjson[self.lastPlayType].get("isSafety", False):
            self.score[int(not self.playTeams.index(self.offense))] += 2
            self.defensePoints = 2
            self.scoringPlay = True
            self.safetyscore = True
            self.down = 0
            self.yardsRemaining = 0
            self.ballPosition = 20
            self.ballTerritory = self.playTeams[int(not self.playTeams.index(self.offense))]

    # check if last play was computed OK
    def _checkConsistency(self, playjson):
        result = True
        if self.ballPosition == 50 and playjson["playStatus"]["lineOfScrimmage"] is not None:
            self.ballTerritory = int(playjson["playStatus"]["lineOfScrimmage"]["team"]["id"])
        # feed bug workaround penalty plays have wrong team in posession
        if "penalty" in playjson.keys():
            playjson["playStatus"]["teamInPossession"]["id"] = str(self.offense)
        if playjson["playStatus"]["lineOfScrimmage"] is not None:
            if (int(playjson["playStatus"]["lineOfScrimmage"]["team"][
                        "id"]) != self.ballTerritory and self.ballTerritory != -1) or \
                    int(playjson["playStatus"]["lineOfScrimmage"]["yardLine"]) != self.ballPosition or \
                    int(playjson["playStatus"]["currentDown"]) != self.down or \
                    int(playjson["playStatus"]["yardsRemaining"]) != self.yardsRemaining or \
                    int(playjson["playStatus"]["teamInPossession"]["id"]) != self.offense and self.offense != 0:
                result = False
        return result

    # gets territory and yardline and returns distance from offense goal line
    def _absyardline(self, territory, yardLine):
        if territory != self.offense:
            return 100 - yardLine
        else:
            return yardLine

    # gets territory and yardline and returns distance from offense goal line
    def _relyardline(self, absYardLine):
        if absYardLine <= 50:
            return self.offense, absYardLine
        else:
            return self.playTeams[int(not self.playTeams.index(self.offense))], 100 - absYardLine

            # process list of subplays

    def _getProgress(self, playjson):
        result = 0
        if "rush" in playjson.keys():
            result = playjson["rush"]["yardsRushed"]
        if "pass" in playjson.keys():
            result = playjson["pass"]["totalYardsGained"]
        return result

        # set the first down and calculate next taget

    def _processFirstDown(self):
        self.down = 1
        if self.offense == self.preOffense and self.isCanceled == False and self.consistent:
            self.conversion = self.preDown
        self.yardsRemaining = 10
        self.fdTargetTerritory = self.ballTerritory
        if self.offense == self.ballTerritory:
            self.fdTargetyardLine = self.ballPosition + 10
        else:
            self.fdTargetyardLine = self.ballPosition - 10
        if self.fdTargetyardLine > 50:
            self.fdTargetyardLine = 100 - self.fdTargetyardLine
            self.fdTargetTerritory = self.playTeams[int(not self.playTeams.index(self.fdTargetTerritory))]
        if self.fdTargetyardLine < 0:
            self.fdTargetyardLine = 0

    # set the first down and calculate next taget
    def _computeYardsRemaining(self):
        if self.scoringPlay:
            self.yardsRemaining = 0
            if self.safetyScore:
                self.ballPosition = 20
            else:
                self.ballPosition = 35
            self.ballTerritory = self.offense
            return
        if self.lastPlayType in ["punt", "kick"]:
            self._processFirstDown()
            return
        if self.down == 0:
            self.yardsRemaining = 0
            return
        if self.offense != self.preOffense:
            self._processFirstDown()
            return
        absPosition = self._absyardline(self.ballTerritory, self.ballPosition)
        absTarget = self._absyardline(self.fdTargetTerritory, self.fdTargetyardLine)
        self.yardsRemaining = absTarget - absPosition
        if self.yardsRemaining > self.ballPosition and self.offense != self.ballTerritory:
            self.yardsRemaining = self.ballPosition
        if self.yardsRemaining <= 0:
            self._processFirstDown()
        return


if __name__ == '__main__':
    filename = "a.json"
    with open(filename, 'r') as f:
        game = json.load(f)
    gameC = NFLPlayContext(game["game"]["awayTeam"]["id"], game["game"]["homeTeam"]["id"], year="2019")
    nplays = 0
    ndrives = 0
    for playjson in game["plays"]:
        if nplays == 23:
            a = 1
            # input(" ")
        print("===================================================================")
        print("processing play:", nplays, playjson["description"])
        result = gameC.play(playjson)
        if not result:
            print("***WARNING: INCONSISTENT WITH LAST PLAY***")
            # input("Press enter to continue")
        print("Play result: Offense: {o}   Down: {d}  Yards remaining: {y} at: {p} of {t}".format(o=gameC.offense,
                                                                                                  d=gameC.down,
                                                                                                  y=gameC.yardsRemaining,
                                                                                                  p=gameC.ballPosition,
                                                                                                  t=gameC.ballTerritory))
        if gameC.conversion != 0 and (gameC.offense == gameC.preOffense):
            print("***Conversion = {c}".format(c=gameC.conversion))
        if ndrives != gameC.drive and gameC.drive != 0:
            print("@@@ New Drive = {d}".format(d=gameC.drive))
            ndrives = gameC.drive
        nplays += 1
    print("Game over! Away Team:{a} Home team:{h}".format(a=gameC.score[0], h=gameC.score[1]))

