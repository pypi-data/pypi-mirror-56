from dateutil.parser import parse
from pprint import pformat
from uuid import UUID

from songkick import queries


def parse_api_datetime(data):
    if data.get("datetime"):
        return parse(data["datetime"])

    if data.get("date"):
        return parse(data["date"])

    return None


class BaseModel:
    def __init__(self, data, api_key=None):
        self.api_data = data
        self.api_key = api_key

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.api_data == other.api_data

        return False

    def __str__(self):
        return pformat(self.api_data)


class IdAndDisplayNameModel(BaseModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.id = data["id"]
        self.display_name = data["displayName"]

    def __str__(self):
        return self.display_name


class SimplifiedArtist(IdAndDisplayNameModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.uri = data["uri"]
        self.musicbrainz_ids = [UUID(i["mbid"]) for i in data["identifier"]]

    def get_upcoming_events(self, **kwargs):
        return queries.ArtistUpcomingEvents(
            api_key=self.api_key, artist_id=self.id, **kwargs
        )

    def get_past_events(self, **kwargs):
        return queries.ArtistPastEvents(
            api_key=self.api_key, artist_id=self.id, **kwargs
        )

    def get_similar_artists(self, **kwargs):
        return queries.SimilarArtists(api_key=self.api_key, artist_id=self.id, **kwargs)


class Artist(SimplifiedArtist):
    def __init__(self, data, api_key=None):

        # TODO: Remove debugging pprint
        from pprint import pprint

        pprint("data")
        pprint(data)
        super().__init__(data, api_key=None)
        if data.get("onTourUntil"):
            self.on_tour_until = parse(data["onTourUntil"]).date()
        else:
            self.on_tour_until = None


class CalendarEntry(BaseModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.event = Event(data["event"], api_key=None)

        try:
            self.attendance = data["reason"]["attendance"]
        except KeyError:
            self.attendance = None

        try:
            self.tracked_artists = [
                Artist(a, api_key=None) for a in data["reason"]["trackedArtist"]
            ]
        except KeyError:
            self.tracked_artists = []

    def __str__(self):
        return str(self.event)


class City(BaseModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.display_name = data["displayName"]
        self.id = data.get("id")
        self.uri = data.get("uri")
        self.country = data["country"]["displayName"]

    def __str__(self):
        return self.display_name


class Event(IdAndDisplayNameModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.uri = data["uri"]
        self.type = data["type"]
        self.status = data["status"]

        self.start = parse_api_datetime(data["start"])
        if "end" in data:
            self.end = parse_api_datetime(data["end"])
        else:
            self.end = None

        self.performances = [Performance(p, api_key=None) for p in data["performance"]]
        self.location = Location(data["location"], api_key=None)
        self.age_restriction = data.get("ageRestriction")

        if data.get("venue"):
            self.venue = SimplifiedVenue(data["venue"], api_key=None)
        else:
            self.venue = None


class Location(BaseModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.city = data["city"]
        self.latitude = data.get("lat")
        self.longitude = data.get("lng")

    def __str__(self):
        return self.city


class MetroArea(IdAndDisplayNameModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.uri = data.get("uri")
        self.country = data["country"]["displayName"]

        try:
            self.state = data["state"]["displayName"]
        except KeyError:
            self.state = None


class Performance(IdAndDisplayNameModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.artist = SimplifiedArtist(data["artist"], api_key=None)
        self.billing_index = data["billingIndex"]
        self.billing = data["billing"]


class SimplifiedVenue(IdAndDisplayNameModel):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.uri = data["uri"]
        self.latitude = data.get("lat")
        self.longitude = data.get("lng")
        self.metro_area = MetroArea(data["metroArea"], api_key=None)

    def get_upcoming_events(self, **kwargs):
        return queries.VenueUpcomingEvents(
            api_key=self.api_key, venue_id=self.id, **kwargs
        )


class Venue(SimplifiedVenue):
    def __init__(self, data, api_key=None):
        super().__init__(data, api_key=None)
        self.city = City(data["city"], api_key=None)
        self.street_address = data.get("street")
        self.postal_code = data.get("zip")
        self.phone = data.get("phone")
        self.website = data.get("website")
        self.capacity = data.get("capacity")
        self.description = data.get("description")
