"""
statsapi module.  Most of the functionality of this module is provided by the decorest module.
"""
from decorest import RestClient, GET, header, query

API_URL = 'https://statsapi.web.nhl.com'


class NHLApiClient(RestClient):
    def __init__(self, endpoint=API_URL):
        super(NHLApiClient, self).__init__(endpoint)

    @GET('api/v1/teams/{team_id}')
    @header('content-type', 'application/json')
    def single_team_data(self, team_id: int) -> str:
        """
        Returns team data for a single team.
        """

    @GET('api/v1/teams')
    @header('content-type', 'application/json')
    def team_data(self) -> str:
        """
        Returns team data for all teams.
        """

    @GET('api/v1/schedule')
    @header('content-type', 'application/json')
    def schedule(self) -> str:
        """
        Returns the schedule for the current day.
        """

    @GET('api/v1/schedule')
    @header('content-type', 'application/json')
    @query('start_date', 'startDate')
    @query('end_date', 'endDate')
    def schedule_range(self, start_date: str, end_date: str) -> str:
        """
        Returns the schedule for a date range.
        """

    @GET('api/v1/teams/{team_id}/stats')
    @header('content-type', 'application/json')
    def single_team_stats(self, team_id: int) -> str:
        """
        Returns the stats for a team.
        """
