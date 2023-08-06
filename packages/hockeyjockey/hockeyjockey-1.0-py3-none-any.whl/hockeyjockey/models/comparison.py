from collections import namedtuple

Comparison = namedtuple('Comparison', ('matchup_id', 'stat_id', 'diff'))


class HJComparison(Comparison):
    pass
