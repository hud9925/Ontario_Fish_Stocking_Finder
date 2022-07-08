import Stocking_methods
from User_methods import User

"""
Basic UI+controller for User interaction with the program
"""
welcome = 'Welcome to the Ontario Fish Stocking locator Program ' \
          'by Daniel Hu! This Program identifies the closest water bodies ' \
          'stocked with fish by the Ontario Ministry of Fish and Wildlife nearest to' \
          ' you!'
print(welcome)
print('')

name = input('What is your name?  ')
print('')

options = (
            "Welcome,"+ ' ' + name + '! '"To continue, please enter a valid address in Ontario!" + ' '
            'Please enter your address in this format: '
            'Unit Number, Street Name, City, Province!')
print(options)
User_details = input("Please enter your address:   ")
print('')

print('Thank you' + ' ' + name + '!' + "Here are the closest waterbodies stocked with"
                                 "fish nearest to you!")

data = Stocking_methods.cleaning_data(
    "Fish_Stocking_data_for_Recreational_Purposes.csv")
new_user = User(name, User_details)
Stocking_methods.distance_sort(data, new_user)

Waterbodies = Stocking_methods.closest_five("Useful_data.csv")
print(Waterbodies)
print(' ')
print(' ')
print(' ')
fish_present = Stocking_methods.fish_species_present(Waterbodies, "Useful_data.csv")

print("The Fish present at the closest Waterbodies contain the following species: ")
print(' ')
print(' ')
print(fish_present)

