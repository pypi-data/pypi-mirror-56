from collections import namedtuple
from hockeyjockey import config

TeamStats = namedtuple('TeamStats', ('evGGARatio',
                                     'faceOffWinPercentage',
                                     'faceOffsLost',
                                     'faceOffsTaken',
                                     'faceOffsWon', 'gamesPlayed',
                                     'goalsAgainstPerGame',
                                     'goalsPerGame',
                                     'losses',
                                     'ot',
                                     'penaltyKillPercentage',
                                     'powerPlayGoals',
                                     'powerPlayGoalsAgainst',
                                     'powerPlayOpportunities',
                                     'powerPlayPercentage',
                                     'ptPctg',
                                     'pts',
                                     'savePctg',
                                     'shootingPctg',
                                     'shotsAllowed',
                                     'shotsPerGame',
                                     'winLeadFirstPer',
                                     'winLeadSecondPer',
                                     'winOppScoreFirst',
                                     'winOutshootOpp',
                                     'winOutshotByOpp',
                                     'winScoreFirst',
                                     'wins',
                                     'pdo'))


class HJTeamStats(TeamStats):
    __slots__ = ()

    def __str__(self):
        fields = sorted(self._fields)
        max_field = max(map(lambda x: len(x), fields))
        acc_width = 0
        team_str = ''

        for f in fields:

            acc_width += (max_field + 1 + config.ts.value_width + 1)
            if acc_width >= config.ts.scr_width:
                acc_width = max_field + 1 + config.ts.value_width + 1
                team_str += '\n'

            team_str += f'{f:>{max_field + 1}}:{getattr(self, f):>{config.ts.value_width + 1}.2f}'

        return team_str
