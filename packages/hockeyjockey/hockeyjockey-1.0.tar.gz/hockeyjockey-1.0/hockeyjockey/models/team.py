from collections import namedtuple
from hockeyjockey import config

Team = namedtuple('Team', ('id', 'name', 'abbrev'))


class HJTeam(Team):
    __slots__ = ()

    def __str__(self):
        return f'{self.id:>{config.t.id_width}} |' \
               f'{self.abbrev:>{config.t.abbrev_width}} |' \
               f'{self.name:>{config.t.name_width}}\n'
