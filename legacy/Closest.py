# import legacy.CSV_Methods as CSV_Methods
# import backend.api.User_methods as User_methods
# import webbrowser
# from geopy.geocoders import Nominatim

# """
# Methods that utilizes Stocking_methods and external APIs 
# """

# def getUserAddress(address):
#     """
#     Uses the Nominatim Service to geocode an address and obtain its coordinates
#     """
#     locator = Nominatim(user_agent='Ontario_Fish_Stocking_Finder')
#     start_location = locator.geocode(address)
#     return start_location


# def Closest_five(address):
#     """
#     Returns a dictionary containing the closest five waterbodies based on the inputted address
#     """
#     unwanted_data = ['X', "Y", "Official_French_Waterbody_Name", "Waterbody_Location_Identifier", "ObjectId",
#                      "Developmental_Stage", "MNRF_District", "Stocking_Year", "Unoffcial_Waterbody_Name",
#                      "Geographic_Township"]
#     data = CSV_Methods.cleaning_data("Fish_Stocking_data_for_Recreational_Purposes.csv", unwanted_data)
#     new_user = User_methods.User('u1', address)
#     CSV_Methods.distance_sort(data, new_user)
#     Waterbodies = CSV_Methods.closest("Useful_data.csv", 5)
#     return Waterbodies

# def getFishPresent(waterbody):
#     """
#     Returns the Fish Stocked at the inputted Waterbody within the dictionary
#     """
#     return CSV_Methods.fish_species_present(Closest_five(waterbody), "Useful_data.csv")[waterbody]

# def getFishPresent2(waterbody):
#     """
#     Returns the fish present at the inputted Waterbody from the csv file
#     """
#     return CSV_Methods.getWaterbody(waterbody, "Useful_data.csv")

# def getWaterBodyCoordinates(waterbody):
#     """
#     Returns the coordinates of the waterbody from the dataset
#     """
#     return CSV_Methods.getWaterbodylocation("Useful_data.csv", waterbody)

# def getDirection(address: list):
#     """
#     Obtains the google map direction between address1 and address 2
#     """

#     webbrowser.open("https://www.google.com/maps/place/"+ address[0] + address[1])

