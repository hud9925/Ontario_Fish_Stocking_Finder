import numpy as np
from geopy.geocoders import Nominatim


class User:
    """
    Determines the User's starting location

    === Representation Invariant ==
    - self.address must be a valid coordinate in Ontario
    """
    name: str
    address: str

    def __init__(self, name, location) -> None:
        """
        Initialize a User with the given name and location

        <name>: name of the user
        <address>: starting location of the user
        """
        self.name = name
        self.address = location

    def starting_location(self) -> tuple[float, float]:
        """
        Takes the User's Inputted address and coverts it into latitude and
        longitude coordinates.

        >>> D = User('Daniel', '587 Violet Street, Waterloo, Ontario')
        >>> D.starting_location() == (43.46837505115125, -80.59676431099521)
        True
        """
        locator = Nominatim(user_agent='Starting Address')
        start_location = locator.geocode(self.address)
        return start_location.latitude, start_location.longitude

    def distance_from_user(self, Latitude, Longitude) -> float:
        """
        Returns the shortest distance between the inputted Latitude and Longitude coordinates
         from the user(Using the Haversine Formula) in kilometers

        <Latitude>: latitude of the waterbody
        <Longitude>: longitude of the waterbody

        >>> D = User('Daniel', '587 Violet Street, Waterloo, Ontario')
        >>> D.starting_location() == (43.46837505115125, -80.59676431099521)
        True
        >>> D.distance_from_user(43.53838, -80.48639) ==  11.825415597935333
        True

        """
        user_location = self.starting_location()
        # convert lat, long coordinates from degrees into radians
        start_lat, end_lat = np.radians(user_location[0]), np.radians(Latitude)
        start_long, end_long = np.radians(user_location[1]), np.radians(Longitude)

        # Haversine formula
        lat_distance, long_distance = end_lat - start_lat, end_long - start_long
        angle = np.sin(lat_distance / 2) ** 2 + np.cos(start_lat) * np.cos(end_lat) * np.sin(long_distance / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(angle))
        r = 6371

        return round(c * r, 2)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
