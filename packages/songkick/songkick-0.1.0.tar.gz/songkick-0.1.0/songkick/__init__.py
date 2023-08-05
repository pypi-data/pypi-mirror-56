__version__ = "0.1.0"

from songkick import queries


class Songkick3:
    def __init__(self, api_key):
        self.api_key = api_key

    def event_search(self, artist_name=None, **kwargs):
        return queries.Events(api_key=self.api_key, artist_name=artist_name, **kwargs)

    def artist_search(self, query, **kwargs):
        return queries.Artists(api_key=self.api_key, query=query, **kwargs)

    def venue_search(self, query, **kwargs):
        return queries.Venues(api_key=self.api_key, query=query, **kwargs)

    def location_search(self, query, **kwargs):
        return queries.Locations(api_key=self.api_key, query=query, **kwargs)

    def get_user_upcoming_calendar(self, username, **kwargs):
        return queries.UserUpcomingCalendar(
            api_key=self.api_key, username=username, **kwargs
        )

    def get_user_past_events(self, username, **kwargs):
        return queries.UserPastEvents(api_key=self.api_key, username=username, **kwargs)

    def get_user_tracked_metro_areas(self, username, **kwargs):
        return queries.UserTrackedMetroAreas(
            api_key=self.api_key, username=username, **kwargs
        )

    def get_user_tracked_artists(self, username, **kwargs):
        return queries.UserTrackedArtists(
            api_key=self.api_key, username=username, **kwargs
        )

    def get_user_muted_artists(self, username, **kwargs):
        return queries.UserMutedArtists(
            api_key=self.api_key, username=username, **kwargs
        )
