from User_methods import User
import pandas as pd

"""
Methods that filters/cleans data from a csv to be more useful 
"""


def cleaning_data(csv, unnecessary_columns: list) -> pd.DataFrame:
    """
    Reads the csv as a Pandas dataframe, removing unwanted columns, and
    returning the result

    :param csv: imported data to be read as a Pandas dataframe

    >>> UnwantedColumns = ['X',"Y", "Official_French_Waterbody_Name","Waterbody_Location_Identifier","ObjectId","Developmental_Stage", "MNRF_District", "Stocking_Year","Unoffcial_Waterbody_Name", "Geographic_Township"]
    >>> len(cleaning_data("Fish_Stocking_data_for_Recreational_Purposes.csv", UnwantedColumns).keys())==5
    True
    """
    return pd.read_csv(csv, header=0).drop(unnecessary_columns, axis='columns')


def distance_sort(dataframe: pd.DataFrame, user: User) -> pd.DataFrame:
    """
    Adds a new column "Distance_from_User," which calculates the distance of
    each waterbody from the inputted User, sorting the entire dataset by
    increasing distance(in km), saving the data to a new csv called
    "Useful_data.csv"
    """
    # Adding a new column detailing distance waterbody is from the user
    dataframe['Distance_from_User'] = user.distance_from_user(dataframe['Latitude'], dataframe['Longitude'])

    # Summing up and sorting by fish species stocked at each waterbody,
    # and then sorted by distance in ascending order
    fish_sum_grouped = \
    dataframe.groupby(["Official_Waterbody_Name", "Distance_from_User", 'Species', "Latitude", "Longitude"])[
        'Number_of_Fish_Stocked'].sum().to_frame().sort_values(by=["Distance_from_User"], ascending=True)
    fish_sum_grouped.to_csv("Useful_data.csv")

    return fish_sum_grouped


def closest(csv, num: int) -> dict:
    """
    Return a dictionary of waterbodies, where the keys are the "Official_Waterbody_Name,"
    and its associated value is the distance from the User
    """
    # Collect the first five closest waterbodies
    data = pd.read_csv(csv, header=0).drop(['Species', 'Number_of_Fish_Stocked'], axis=1).drop_duplicates().iloc[:num]

    # Convert into python dictionary with "Official_Waterbody_Name" as the
    # keys, and "Distance_from_User" as the key's value

    return data.set_index("Official_Waterbody_Name").to_dict()['Distance_from_User']


def getWaterbodylocation(csv, waterbody) -> tuple[float, float]:
    """
    Returns the lat and long coordinates
    """
    data = pd.read_csv(csv, index_col=None, header=0).drop(["Distance_from_User", "Species"], axis="columns").drop_duplicates()
    find_waterbody = (data.loc[data["Official_Waterbody_Name"] == waterbody]["Latitude"],
                      data.loc[data["Official_Waterbody_Name"] == waterbody]["Longitude"])
    return find_waterbody



def getWaterbody(waterbody, csv) -> any:
    """
    Removes all Entries within the pandas DataFrame except for the desired Waterbody
    """
    # Get indexes where name column doesn't have value john
    data = pd.read_csv(csv, index_col=None, header=0).drop("Distance_from_User", axis="columns")
    data = data.loc[data['Official_Waterbody_Name'] == waterbody]
    fish_species = data.groupby('Official_Waterbody_Name')[['Species', 'Number_of_Fish_Stocked']] \
        .apply(lambda x: x.set_index('Species').to_dict(orient='index')).to_dict()
    return fish_species


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
    >>> print(fish_species_present(bodies, "Useful_data.csv")['Humber River'])
    """
    data = pd.read_csv(csv, header=0).iloc[:50]
    fish_species = data.groupby('Official_Waterbody_Name')[['Species', 'Number_of_Fish_Stocked']] \
        .apply(lambda x: x.set_index('Species').to_dict(orient='index')).to_dict()
    desired_data = dict((x, fish_species[x]) for x in Waterbodies.keys() if x in fish_species)
    return desired_data


if __name__ == '__main__':
    import doctest

    doctest.testmod()
