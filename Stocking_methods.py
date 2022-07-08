
from User_methods import User
import pandas as pd
"""
Filters data obtained from 'Fish_Stocking_data_for_Recreational_Purposes'.csv
to be more useful
"""

def cleaning_data(csv) -> pd.DataFrame:
    """
    Reads the csv as a Pandas dataframe, removing unwanted columns, and
    returning the result as a Pandas dataframe

    :param csv: imported data to be read as a Pandas dataframe
    >>> len(cleaning_data("Fish_Stocking_data_for_Recreational_Purposes.csv").keys())==5
    True
    """

    unnecessary_columns = ['X',"Y", "Official_French_Waterbody_Name",
                           "Waterbody_Location_Identifier","ObjectId",
                           "Developmental_Stage", 'MNRF_District', 'Stocking_Year',
                            'Unoffcial_Waterbody_Name', 'Geographic_Township'
                           ]
    return pd.read_csv(csv, header=0).drop(unnecessary_columns, axis='columns')

def distance_sort(dataframe: pd.DataFrame, user: User) -> pd.DataFrame:
    """
    Adds a new column "Distance_from_User," which calculates the distance of
    each waterbody from the inputted User, sorting the entire dataset by
    increasing distance(in km), saving the data to a new csv called
    "Useful_data.csv"

    >>> Sample_User = User('Daniel', 'Humber Bay Arch Bridge, Toronto Ontario')
    >>> data = cleaning_data("Fish_Stocking_data_for_Recreational_Purposes.csv")
    # >>> distance_sort(data, Sample_User)[]

    """
    # Adding a new column detailing distance waterbody is from the user
    dataframe['Distance_from_User'] = user.distance_from_user(dataframe['Latitude'], dataframe['Longitude'])

    # Summing up and sorting by fish species stocked at each waterbody,
    # and then sorted by distance in ascending order
    fish_sum_grouped = dataframe.groupby(["Official_Waterbody_Name", "Distance_from_User", 'Species'])['Number_of_Fish_Stocked'].sum().to_frame().sort_values(by=["Distance_from_User"], ascending=True)
    fish_sum_grouped.to_csv("Useful_data.csv")

    return fish_sum_grouped

def closest_five(csv) -> dict:
    """
    Return a dictionary of waterbodies, where the keys are the "Official_Waterbody_Name,"
    and its associated value is the distance from the User
    """

    # Collect the first five closest waterbodies
    data = pd.read_csv(csv, header=0).drop(['Species','Number_of_Fish_Stocked'], axis=1).drop_duplicates().iloc[:5]

    # Convert into python dictionary with "Official_Waterbody_Name" as the
    # keys, and "Distance_from_User" as the key's value
    return data.set_index("Official_Waterbody_Name").to_dict()['Distance_from_User']

def get_distance(waterbody: string, Waterbody_dict: dict) -> int:
    """
    Returns the distance of the inputted waterbody from the waterbody dictionary
    """
    return Waterbody_dict[waterbody]

def fish_species_present(Waterbodies: dict, csv) -> dict:
    """
    Returns A dictionary of the fish species present at the inputted Waterbodies

    Waterbodies must be valid stocked waterbodies in Ontaro
    :param Waterbodies: a dictionary of stocked waterbodies

        # Testing dataset where each waterbody only has one specie stocked
    >>> bodies = {'Conestogo River': 11.825415597935333, 'Carroll Creek': 22.869145715961995, 'Mill Creek': 25.839009975762192, 'Fairy Lake': 47.50652814669023, 'Spencer Creek': 58.41003210962975}
    >>> len(fish_species_present(bodies, "Useful_data.csv").keys()) == 5
    True

        # Testing dataset where waterbody could contain multiple different stocked species
    >>> bodies = {'Humber River': 0.0824854586202612, 'Don River': 10.685839574554205, 'Credit River': 12.864008158286934, 'Lake Aquitaine': 23.27471065674293, 'Heart Lake': 28.71361733202099}
    >>> len(fish_species_present(bodies, "Useful_data.csv")['Humber River']) == 3
    True

    """
    data = pd.read_csv(csv, header =0).iloc[:50]
    fish_species = data.groupby('Official_Waterbody_Name')[['Species', 'Number_of_Fish_Stocked']]\
        .apply(lambda x: x.set_index('Species').to_dict(orient = 'index')).to_dict()
    desired_data = dict((x, fish_species[x]) for x in Waterbodies.keys() if x in fish_species)
    return desired_data

if __name__ == '__main__':
    import doctest

    doctest.testmod()




