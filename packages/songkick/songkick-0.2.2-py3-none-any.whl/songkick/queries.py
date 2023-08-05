import requests

from songkick import models

URL = "https://api.songkick.com/api/3.0"


class BaseQuery:
    def __init__(self, api_key, **params):
        self.api_key = api_key
        self.params = params
        self.params["apikey"] = api_key
        self._results = []

    def get_url(self):
        return self.url

    def __iter__(self):
        return self

    def __next__(self):
        if not self._results:
            response = requests.get(self.get_url(), params=self.params)
            response.raise_for_status()
            parsed_response = response.json()

            if not parsed_response["resultsPage"]["results"]:
                raise StopIteration

            for result_data in self._get_result_data(parsed_response):
                self._results.append(self._build_result(result_data))

            # Get params ready for next page.
            self.params["page"] = parsed_response["resultsPage"]["page"] + 1

        return self._results.pop(0)

    def _get_result_data(self, parsed_response):
        if self.result_key not in parsed_response["resultsPage"]["results"]:
            available_keys = ", ".join(parsed_response["resultsPage"]["results"].keys())
            raise RuntimeError(
                f"Key {self.result_key} not in results; available keys are {available_keys}"
            )

        return [r for r in parsed_response["resultsPage"]["results"][self.result_key]]

    def _build_result(self, result_data):
        return self.model_class(result_data, api_key=self.api_key)


class Events(BaseQuery):
    url = URL + "/events.json"
    result_key = "event"
    model_class = models.Event


class Artists(BaseQuery):
    url = URL + "/search/artists.json"
    result_key = "artist"
    model_class = models.Artist


class Venues(BaseQuery):
    url = URL + "/search/venues.json"
    result_key = "venue"
    model_class = models.Venue


class Locations(BaseQuery):
    url = URL + "/search/locations.json"
    result_key = "location"

    def _build_result(self, result_data):
        return (
            models.City(result_data["city"], self.api_key),
            models.MetroArea(result_data["metroArea"], self.api_key),
        )


class ArtistUpcomingEvents(Events):
    def __init__(self, api_key, artist_id, **kwargs):
        super().__init__(api_key, **kwargs)
        self.artist_id = artist_id

    def get_url(self):
        return f"{URL}/artists/{self.artist_id}/calendar.json"


class ArtistPastEvents(ArtistUpcomingEvents):
    def get_url(self):
        return f"{URL}/artists/{self.artist_id}/gigography.json"


class SimilarArtists(Artists):
    def __init__(self, api_key, artist_id, **kwargs):
        super().__init__(api_key, **kwargs)
        self.artist_id = artist_id

    def get_url(self):
        return f"{URL}/artists/{self.artist_id}/similar_artists.json"


class VenueUpcomingEvents(Events):
    def __init__(self, api_key, venue_id, **kwargs):
        super().__init__(api_key, **kwargs)
        self.venue_id = venue_id

    def get_url(self):
        return f"{URL}/venues/{self.venue_id}/calendar.json"


class UserUpcomingCalendar(BaseQuery):
    result_key = "calendarEntry"
    model_class = models.CalendarEntry

    def __init__(self, api_key, username, **kwargs):
        super().__init__(api_key, **kwargs)
        self.username = username

    def get_url(self):
        return f"{URL}/users/{self.username}/calendar.json"


class UserPastEvents(Events):
    def __init__(self, api_key, username, **kwargs):
        super().__init__(api_key, **kwargs)
        self.username = username

    def get_url(self):
        return f"{URL}/users/{self.username}/gigography.json"


class UserTrackedMetroAreas(BaseQuery):
    result_key = "metroArea"
    model_class = models.MetroArea

    def __init__(self, api_key, username, **kwargs):
        super().__init__(api_key, **kwargs)
        self.username = username

    def get_url(self):
        return f"{URL}/users/{self.username}/metro_areas/tracked.json"


class UserTrackedArtists(Artists):
    def __init__(self, api_key, username, **kwargs):
        super().__init__(api_key, **kwargs)
        self.username = username

    def get_url(self):
        return f"{URL}/users/{self.username}/artists/tracked.json"


class UserMutedArtists(UserTrackedArtists):
    def get_url(self):
        return f"{URL}/users/{self.username}/artists/muted.json"
