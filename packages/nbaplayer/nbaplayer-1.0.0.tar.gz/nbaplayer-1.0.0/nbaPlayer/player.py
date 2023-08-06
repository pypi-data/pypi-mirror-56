from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from operator import attrgetter
from nba_api.stats.static import players
import json
import pprint

# ? endpoint information: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/commonplayerinfo.md


class Player:
    # Constructor initalises player stats and populates them with essential details e.g. firstname and lastname
    def __init__(self, player_id):
        self.playerStats = {}
        self.id = player_id
        rawDetails = commonplayerinfo.CommonPlayerInfo(
            player_id=self.id).get_dict()['resultSets'][0]
        print(rawDetails['headers'].index('FIRST_NAME'))
        self.playerStats['firstName'] = rawDetails['rowSet'][0][rawDetails['headers'].index(
            'FIRST_NAME')]
        self.playerStats['lastName'] = rawDetails['rowSet'][0][rawDetails['headers'].index(
            'LAST_NAME')]

    def getStat(self, statString):
        return self.playerStats[statString]

    def setStats(self, statList):
        # get latest season info
        seasonInfo = playercareerstats.PlayerCareerStats(
            player_id=self.id).get_dict()["resultSets"][0]

        for statString in statList:
            # identify position of required element by referencing the Headers object
            i = seasonInfo["headers"].index(statString)

            # add stat to playerStats dict
            self.playerStats[statString] = seasonInfo['rowSet'][-1][i]


harden_id = players.find_players_by_last_name("Harden")[0]["id"]

jamesHarden = Player(harden_id)
jamesHarden.setStats(
    ['PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT'])
print(jamesHarden.playerStats)
