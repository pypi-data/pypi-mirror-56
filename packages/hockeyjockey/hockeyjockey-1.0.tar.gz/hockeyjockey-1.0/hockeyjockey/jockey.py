"""
jockey module is the main module for hockeyjockey
"""
import os
import json

import colors as col
import hockeyjockey.api as api
import hockeyjockey.models as mod
from hockeyjockey.menu import Menu
import hockeyjockey.utilities as ut
from hockeyjockey import config as cfg


class Jockey(object):
    """
    The main HockeyJockey class. Takes care of instantiating Menus, loading data, and performing calculations.
    """

    def __init__(self) -> None:
        """
        Initializer
        """
        # Init menus
        self.menu_main = None
        self.menu_match = None
        self.menu_stats = None
        self.menu_teams = None

        # Stored hockey data
        self.matchups = []
        self.pretty_matchups = []
        self.teams = []
        self.stats = {}
        self.ranked_stat = None
        self.rankings = {}
        self.comparisons = []

        # Files and paths
        self.use_cached_matchups = False
        self.use_cached_stats = False
        self.hj_dir = None
        self.teams_file = None
        self.stats_file = None
        self.matchups_file = None

        # Loaders
        self.use_cached()
        self.load_filepaths()
        self.load_menus()
        self.load_teams()
        self.load_stats()
        self.load_cached_matchups()

    def use_cached(self):
        """
        Stores the user's preference as to whether or not they wish to use data that has been cached to disk.

        :return: None.
        """
        self.use_cached_stats, self.use_cached_matchups = Menu.prompt_for_cached()

    def load_filepaths(self):
        """
        Creates the hockeyjockey directory and files for caching data.

        :return: None.
        """
        self.hj_dir = ut.get_hj_dir()
        if self.hj_dir:
            self.teams_file = ut.get_hj_file_path(self.hj_dir, cfg.file.teams_file)
            self.stats_file = ut.get_hj_file_path(self.hj_dir, cfg.file.stats_file)
            self.matchups_file = ut.get_hj_file_path(self.hj_dir, cfg.file.matchups_file)

    def load_menus(self) -> None:
        """
        Loads the HockeyJockey Menu objects. This represents the main menu structure of HockeyJockey.

        :return: None.
        """

        print('Loading menus... ', end='')

        self.menu_teams = Menu('Teams', 'Teams menu',
                               [{'name': 'Print Teams', 'payload': self.print_teams}],
                               'Make your selection: ')

        self.menu_stats = Menu('Stats', 'Stats menu',
                               [{'name': 'Reload Stats', 'payload': self.reload_stats},
                                {'name': 'Rank Matchups by Single Statistic',
                                 'payload': self.compare_stat},
                                {'name': 'Print Stats',
                                 'payload': self.print_stats}],
                               'Make your selection: ')

        self.menu_match = Menu('Matchups', 'Matchups menu',
                               [{'name': 'Load Today\'s Matchups', 'payload': self.load_matchups_today},
                                {'name': 'Load Upcoming Friday/Saturday', 'payload': self.load_matchups_fri_sat},
                                {'name': 'Load Custom Date Range', 'payload': self.load_matchups_custom},
                                {'name': 'Print Matchups', 'payload': self.print_matchups},
                                ],
                               'Make your selection: ')

        self.menu_main = Menu('Hockey Jockey', 'Main Menu',
                              [{'name': 'Matchups', 'payload': self.menu_match},
                               {'name': 'Teams', 'payload': self.menu_teams},
                               {'name': 'Stats', 'payload': self.menu_stats},
                               {'name': 'Exit', 'payload': Menu.exit_}],
                              'Make your selection: ')
        print('Done.')

    # LOADING FUNCTIONS
    def load_teams(self) -> None:
        """
        Loads the teams from disk if they exist, otherwise loads the teams from the internet (statsapi).

        :return: None.
        """
        # Disk load
        if os.path.exists(self.teams_file):
            print('Loading teams from disk... ', end='')

            # DESERIALIZE
            self.teams = ut.deserialize(self.teams_file)
            if self.teams:
                print('Done.')
                return

        # Download
        print('Downloading teams... ', end='')
        client = api.NHLApiClient()
        teams = json.loads(client.team_data())

        for team in teams['teams']:
            hj_team = mod.HJTeam(team['id'], team['name'], team['abbreviation'])
            self.teams.append(hj_team)

        # SERIALIZE
        with open(self.teams_file, 'w+') as fh:
            fh.write(repr(self.teams))

        print('Done.')

    def load_matchups_custom(self, start_date: str, end_date: str) -> None:
        """
        Loads the matchups for a custom date range.

        :param start_date: String-formatted start date.
        :param end_date: String-formatted end date.
        :return: None.
        """
        print(f'Loading matchups between {start_date} and {end_date}...', end='')
        client = api.NHLApiClient()
        schedule = json.loads(client.schedule_range(start_date, end_date))
        self.schedule_to_matchups(schedule)
        print('Done.')

    def load_matchups_today(self) -> None:
        """
        Loads the matchups for today's date.

        :return: None.
        """
        print('Loading matchups for today...', end='')
        client = api.NHLApiClient()
        schedule = json.loads(client.schedule())
        self.schedule_to_matchups(schedule)
        print('Done.')

    def load_matchups_fri_sat(self) -> None:
        """
        Loads the matchups for this (or the next) Friday and Saturday's games.
        :return: None.
        """
        fri, sat = ut.closest_fri_sat()
        self.load_matchups_custom(fri, sat)

    def load_cached_matchups(self) -> None:
        """
        Loads the matchups cached to disk. If loading fails, loads the current day's matchups from the internet
        (statsapi)

        :return: None.
        """
        # Clear existing matchups
        self.matchups.clear()

        # Disk load
        if self.use_cached_matchups and os.path.exists(self.matchups_file):
            print('Loading matchups from disk... ', end='')

            # DESERIALIZE
            self.matchups = ut.deserialize(self.matchups_file)
            if self.matchups:
                self.prettify_matchups()
                print('Done.')
                return

        # Download - default to today's matchups
        self.load_matchups_today()

    def schedule_to_matchups(self, schedule: 'json string') -> None:
        """
        Clears the current matchups and reloads from json. Takes the json schedule returned from the api and loads it
        into the matchups list.  Also populates the disk cache.

        :param schedule: json-formatted scheudule
        :return: None.
        """
        self.matchups.clear()

        for date in schedule['dates']:
            for game in date['games']:
                self.matchups.append(mod.HJMatchup(
                    game['teams']['home']['team']['id'],
                    game['teams']['away']['team']['id'],
                    date['date']))

        if self.matchups:
            self.prettify_matchups()

        # SERIALIZE
        with open(self.matchups_file, 'w+') as fh:
            fh.write(repr(self.matchups))

    def prettify_matchups(self):
        """
        Makes a 'pretty' version of the matchups list attribute for display purposes. Teams are represented by their
        abbreviation instead of their id.

        :return: None.
        """
        if not self.matchups:
            print('There are no matchups. Cannot make nothing pretty.')
            return

        if not self.teams:
            print('No teams have been loaded. Teams are required for pretty matchups.')
            return

        self.pretty_matchups.clear()
        for m in self.matchups:
            a_abbrev = next(iter(t.abbrev for t in self.teams if m.away_id == t.id))
            h_abbrev = next(iter(t.abbrev for t in self.teams if m.home_id == t.id))
            self.pretty_matchups.append(m._replace(away_id=a_abbrev, home_id=h_abbrev))

    def load_stats(self) -> None:
        """
        Loads the latest statistics from the internet (statsapi).

        :return: None.
        """
        if self.use_cached_stats and os.path.exists(self.stats_file):
            print('Loading stats from disk...', end='')
            # DESERIALIZE
            self.stats = ut.deserialize(self.stats_file)
            if self.stats:
                return

        print('Downloading stats... ', end='')
        client = api.NHLApiClient()
        for team in self.teams:
            stats = json.loads(client.single_team_stats(team.id))

            team_stats = None

            for stat_type in stats['stats']:
                if stat_type['type']['displayName'] == 'statsSingleSeason':
                    for split in stat_type['splits']:
                        # Add additional calculated stats here:
                        pdo = ut.calc_pdo(ut.floatize(split['stat']['shootingPctg']),
                                          ut.floatize(split['stat']['savePctg']))

                        team_stats = mod.HJTeamStats(pdo=ut.floatize(pdo),
                                                     **{k: ut.floatize(v) for k, v in split['stat'].items()})
            self.stats[team.id] = team_stats

        # SERIALIZE
        with open(self.stats_file, 'w+') as fh:
            fh.write(repr(self.stats))

        print('Done.')

    def reload_stats(self):
        """
        Reloads statistical data from the internet and overwrites the current cached data on disk. This also clears any
        current statistical comparisons.

        :return: None.
        """
        print('Reloading stats...', end='')

        # Clear some existing data
        self.comparisons.clear()
        self.rankings.clear()
        self.ranked_stat = None

        self.use_cached_stats = False
        self.load_stats()

        print('Done.')

    # CALCULATING/RANKING FUNCTIONS
    def compare_stat(self, stat_id: int) -> None:
        """
        Iterates through the Matchups (hockey games) currently in memory and compares a single statistic (stat_id)
        between each pairing of home and away team. The results are stored as HJComparison tuples in the 'comparisons'
        list attribute.

        :param stat_id: The integer index of the stat to be compared.
        :return: None.
        """
        fields = sorted(mod.HJTeamStats._fields)
        stat_name = fields[stat_id]

        if self.matchups:
            for i, m in enumerate(self.matchups):
                a_id, h_id = m.away_id, m.home_id
                a_stat = getattr(self.stats[a_id], stat_name)
                h_stat = getattr(self.stats[h_id], stat_name)
                diff = h_stat - a_stat
                self.comparisons.append(mod.HJComparison(i, stat_id, diff))

            # Rank the matchups for use in confidence pools
            self.rank_matchups_by_stat(stat_id)
        else:
            print('No matchups have been loaded yet. Load some from the matchups menu first.')

    def rank_matchups_by_stat(self, stat_id: int) -> None:
        """
        Ranks a group of stats by stat_id and stores in rankings attribute.

        :param stat_id: The integer index of the stat to be ranked.
        :return: None.
        """
        comps = [comp for comp in self.comparisons if comp.stat_id == stat_id]

        if comps:
            comps = sorted(comps, key=lambda x: abs(x.diff))

            for i, comp in enumerate(comps, start=1):
                self.rankings[comp.matchup_id] = i

            self.ranked_stat = stat_id
            self.print_ranked()
        else:
            print('No comparisons have been calculated for this stat. Nothing to rank.')

    # PRINTING FUNCTIONS
    def print_teams(self) -> None:
        """
        Prints a list of the teams that are loaded.

        :return: None.
        """

        print()
        print(
            f'{"Team ID":>{cfg.t.id_width}} |{"Abbreviation":>{cfg.t.abbrev_width}} |{"Team Name":>{cfg.t.name_width}}')
        print('-' * (cfg.t.id_width + cfg.t.abbrev_width + cfg.t.name_width + 4))
        print(*sorted(self.teams, key=lambda x: x.name), sep='')
        print()

    def print_matchups(self, pretty: bool = True) -> None:
        """
        Prints a list of the matchups that are loaded.

        :param: pretty: If True, print the matchup with the team abbreviation.  If false, shows the team id.
        :return: None.
        """
        print()
        print(f'{"Date":>{cfg.m.date_width}} |{"Away":>{cfg.m.team_width}} |{"Home":>{cfg.m.team_width}}')
        print('-' * (cfg.m.date_width + cfg.m.team_width * 2 + 4))
        if pretty:
            print(*self.pretty_matchups, sep='')
            print()
        else:
            print(*self.matchups, sep='')
            print()

    def print_stats(self) -> None:
        """
        Prints a list of the stats for each team.

        :return: None.
        """

        if not self.stats:
            print('No stats have been loaded. Cannot print.')
        else:
            print()
            for t in sorted(self.teams, key=lambda x: x.name):
                cur_stats = self.stats[t.id]
                title_str = f'Stats for team: {t.name:<{cfg.ts.field_width}}'
                print(f'{title_str:^{cfg.ts.scr_width}}')
                print(f'-' * cfg.ts.scr_width)
                print(cur_stats)
                print()
            print()

    def print_ranked(self) -> None:
        """
        Prints the matchups as they are currently ranked.

        :return: None.
        """
        # Ranked stat can be 0, hence the 'not None' check here:
        if self.ranked_stat is not None:
            desired_r_wid = cfg.r.rank_width
            desired_h_wid = desired_a_wid = cfg.r.team_width

            print()
            print(
                f'{"Away":^{cfg.r.team_width}}|'
                f'{"Home":^{cfg.r.team_width}}|'
                f'{"Diff":>{cfg.r.diff_width}} | '
                f'{"Rank":>{cfg.r.rank_width}}')

            print('-' * (cfg.r.team_width * 2 + 5 + cfg.r.diff_width + cfg.r.rank_width))

            for i, m in enumerate(self.matchups):

                a_team = next(iter(team.abbrev for team in self.teams if team.id == m.away_id))
                h_team = next(iter(team.abbrev for team in self.teams if team.id == m.home_id))
                diff = next(iter(comp.diff for comp in self.comparisons if
                                 comp.stat_id == self.ranked_stat and comp.matchup_id == i))

                rank = col.color(str(self.rankings[i]), fg='green')
                rank_wid = desired_r_wid - col.ansilen(rank) + len(rank)

                h_wid = None
                a_wid = None

                if diff >= 0:
                    h_team = col.color(h_team, fg='green')
                    # Padding
                    h_wid = desired_h_wid - col.ansilen(h_team) + len(h_team)

                else:
                    a_team = col.color(a_team, fg='green')
                    # Padding
                    a_wid = desired_a_wid - col.ansilen(a_team) + len(a_team)

                print(
                    f'{a_team:^{a_wid or desired_a_wid}}|'
                    f'{h_team:^{h_wid or desired_h_wid}}|'
                    f'{abs(diff):>{cfg.r.diff_width}.2f} | '
                    f'{rank:>{rank_wid or desired_r_wid}}')

            print()
        else:
            print('No stat is currently ranked. Cannot print.')
