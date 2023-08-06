"""
Configurations.
"""
from collections import namedtuple

glbl_scr_width = 120

# Print formatting configuration
TeamStatsConfig = namedtuple('TeamStatsConfig', ('scr_width', 'field_width', 'value_width'))
ts = TeamStatsConfig(scr_width=glbl_scr_width, field_width=22, value_width=7)

MatchupConfig = namedtuple('MatchupConfig', ('scr_width', 'date_width', 'team_width'))
m = MatchupConfig(scr_width=glbl_scr_width, date_width=11, team_width=8)

TeamConfig = namedtuple('TeamConfig', ('scr_width', 'id_width', 'name_width', 'abbrev_width'))
t = TeamConfig(scr_width=glbl_scr_width, id_width=8, name_width=22, abbrev_width=13)

RanksConfig = namedtuple('RanksConfig', ('scr_width', 'rank_width', 'team_width', 'diff_width'))
r = RanksConfig(scr_width=glbl_scr_width, rank_width=5, team_width=6, diff_width=9)

DateConfig = namedtuple('DateConfig', ('date_fmt', 'date_str'))
date = DateConfig(date_fmt='%Y-%m-%d', date_str='YYYY-MM-DD')

FileConfig = namedtuple('FileConfig', ('data_dir_loc', 'data_dir_name', 'teams_file', 'matchups_file', 'stats_file'))
file = FileConfig(data_dir_loc='~',
                  data_dir_name='hj_data',
                  teams_file='teams.data',
                  matchups_file='matchups.data',
                  stats_file='stats.data')
