from geopy.geocoders import Nominatim
import math
import os
import psycopg2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Database connection details
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


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
        Converts the inputted address into latitude and longitude coordinates; returning a tuple of lat and long
        """
        try:
            locator = Nominatim(user_agent='Ontario_Fish_Stocking_Finder')
            location = locator.geocode(self.address)
            return (location.latitude, location.longitude)
        except GeocoderTimedOut:
            print("Error: Geocoding timed out.")
            return None

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two points on the Earth.
        :param lat1: Latitude of point 1.
        :param lon1: Longitude of point 1.
        :param lat2: Latitude of point 2.
        :param lon2: Longitude of point 2.
        :return: Distance in kilometers.
        """
        R = 6371  # Radius of the Earth in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def find_closest_waterbodies(self, limit=5) -> float:
        """
        Finds the closest waterbodies to the user's location.
        :param limit: Number of closest waterbodies to return.
        :return: List of tuples containing waterbody name and distance.
        True

        """
        user_location = self.starting_location()
        if not user_location:
            return None
        
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("SELECT name, latitude, longitude FROM waterbodies")
        waterbodies = cursor.fetchall()

        waterbodies_with_distances = []
        for waterbody in waterbodies:
            name, lat, lon = waterbody
            distance = self.haversine(user_location[0], user_location[1], lat, lon)
            waterbodies_with_distances.append((name, distance))

        waterbodies_with_distances.sort(key=lambda x: x[1])
        
        connection.close()
        return waterbodies_with_distances[:limit]

    def getWaterbody(self, waterbody_name: str) -> dict:
        """
        Retrieve the fish data for a specified waterbody from the database.

        <waterbody_name>: The name of the waterbody to look up

        Returns a dictionary where keys are the fish species and values are
        the number of fish stocked.
        """
         # Load environment variables
        load_dotenv()

        # Connect to PostgreSQL using psycopg2
        try:
            connection = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )

            cursor = connection.cursor()
            query = f"""
            SELECT fs.name AS species, se.number_of_fish
            FROM stocking_events se
            JOIN waterbodies wb ON se.waterbody_id = wb.id
            JOIN fish_species fs ON se.species_id = fs.id
            WHERE wb.name = %s
            """
            cursor.execute(query, (waterbody_name,))
            rows = cursor.fetchall()

            fish_data = {row[0]: {'Number_of_Fish_Stocked': row[1]} for row in rows}

        except Exception as e:
            print(f"Error fetching data from database: {e}")
            fish_data = {}
        finally:
            if connection:
                cursor.close()
                connection.close()

        return fish_data

if __name__ == '__main__':
    # testing the closest waterbodies; should be Conestogo River, Carroll Creek, Mill Creek, and Unnamed Waterbody, and Fairy Lake
    user = User('Daniel', '587 Violet Street, Waterloo, Ontario')
    closest_waterbodies = user.find_closest_waterbodies()

    # Correctly iterating through each waterbody to get the fish data
    for waterbody in closest_waterbodies:
        fish_data = user.getWaterbody(waterbody[0])
        print(f"Fish stocked in {waterbody[0]} ({waterbody[1]} km away): {fish_data}")
    