from collections import namedtuple
from hockeyjockey import config

Matchup = namedtuple('Matchup', ('home_id', 'away_id', 'date'))


class HJMatchup(Matchup):
    __slots__ = ()

    def __str__(self):
        return f'{self.date:>{config.m.date_width}} |' \
               f'{self.away_id:>{config.m.team_width}} |' \
               f'{self.home_id:>{config.m.team_width}}\n'
