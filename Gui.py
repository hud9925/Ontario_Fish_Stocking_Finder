import tkinter as tk
from tkinter import ttk
import json
import Closest
from ttkthemes.themed_tk import ThemedTk
title_font = ("Times Bold", 14)

class FishStockerGui(ThemedTk):

    def __init__(self):
        ThemedTk.__init__(self)
        #tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Ontario Fish Stocking Finder")
        self.container = tk.Frame()
        self.set_theme("arc")


        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Frame in [main_menu, closest_search_page, closest_waterbodies, WaterBodyInfo, stat_page]:
            frame = Frame(self.container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = main_menu(self.container, self)

        self.frames[main_menu] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = None
        self.show_frame(main_menu)

    def show_frame(self, key):
        frame = self.frames[key]
        frame.tkraise()

    def get_page(self, page):
        return self.frames[page]


class main_menu(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Main Menu", font=title_font)
        label.pack(pady=10, padx=10)

        option1 = ttk.Button(self, text="Find Closest stocked Bodies of Water",
                             command=lambda: controller.show_frame(closest_search_page))
        option2 = ttk.Button(self, text="Ontario Fish Stocking Stats", command=lambda: controller.show_frame(stat_page))
        option1.pack()
        option2.pack()


class closest_search_page(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        address = tk.StringVar()

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Enter A Valid Ontario Address\n"
                                     "Please Enter it in this format:"
                                     "(Street Number, Street Name, City) ")
        label.pack(fill='x', expand=True)

        address_entry = ttk.Entry(self, textvariable=address)

        address_entry.pack(fill='x', expand=True)
        address_entry.focus()

        # Search Button
        search_button = ttk.Button(self, text="Search!", command=lambda: [controller.show_frame(closest_waterbodies),
                                                                          self.SearchClicked(address_entry.get()),
                                                                          controller.frames[
                                                                              closest_waterbodies].updateData()])
        search_button.pack(fill='x', expand=True, pady=10)

        return_menu_button = ttk.Button(self, text="Return to Menu",
                                        command=lambda: controller.show_frame(main_menu))
        return_menu_button.pack()

    def SearchClicked(self, address) -> None:
        """
        Inputs the User's address and obtain the Closest Five Waterbodies
        """
        dict_of_Waterbodies = Closest.Closest_five(Closest.getUserAddress(address))

        # save closest Waterbodies to a txt file
        with open("Waterbodies.txt", 'w') as file:
            file.write(json.dumps(dict_of_Waterbodies))


class closest_waterbodies(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="   Here are the Closest Stocked Waterbodies to You! " + "\n"
                                         "To See the Fish Stocked at each"
                                         " waterbody, click the waterbody name",
                          font=("Time Bold", 12))
        # Create the waterbody tree
        treeview = ttk.Treeview(self)
        treeview['columns'] = ("Waterbody_Name", "Distance_From_User", "Fish_Present")
        treeview.column("Waterbody_Name", anchor=tk.W, width=120)
        treeview.column("Distance_From_User", anchor=tk.CENTER, width=200)

        # headings
        treeview.heading("Waterbody_Name", text="Waterbody Name")
        treeview.heading("Distance_From_User", text="Distance From You (in KM)")
        treeview.pack(pady=20)

        self.treeview = treeview

        # binding
        self.treeview.bind("<ButtonRelease-1>", self.click)

        return_menu_button = ttk.Button(self, text="Return to Menu",
                                        command=lambda: controller.show_frame(main_menu))
        return_menu_button.pack(side="bottom")

        label.pack(side="bottom")

    def updateData(self):
        """
        Updates the data within the treeview
        """
        with open("Waterbodies.txt", 'r') as file:
            user_dict = json.load(file)
            for record in self.treeview.get_children():
                self.treeview.delete(record)
            for waterbody in user_dict:
                self.treeview.insert(parent='', index='end', text='', values=(waterbody, user_dict[waterbody]))

    def click(self, event):
        selected_item = self.treeview.focus()
        waterbody_name = self.treeview.item(selected_item)["values"][0]
        print(Closest.getWaterBodyCoordinates(waterbody_name))
        with open("FishPresent.txt", "a+") as file:
            file.truncate(0)
            file.write(waterbody_name + "\n")
            file.write(json.dumps(Closest.getFishPresent2(self.treeview.item(selected_item)["values"][0])))
        self.controller.show_frame(WaterBodyInfo)
        self.controller.frames[WaterBodyInfo].updateTree()


class WaterBodyInfo(tk.Frame):
    """
    Displays the Fish Present At the Given Waterbody
    """

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        tree = ttk.Treeview(self)
        tree['columns'] = ("Fish Present", "Total Number Stocked")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Fish Present", anchor=tk.W, width=120)
        tree.column("Total Number Stocked", anchor=tk.CENTER, width=200)

        # headings
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Fish Present", text="Fish Species")
        tree.heading("Total Number Stocked", text="Total Number of Fish Stocked")
        tree.pack(pady=20)

        self.tree = tree

        get_direction = ttk.Button(self, text="Get Direction to Waterbody!", command= lambda: self.get_direction())

        return_to_waterbodies = ttk.Button(self, text="Return to Table of Waterbodies",
                                           command=lambda: controller.show_frame(closest_waterbodies))

        get_direction.pack()

        return_to_waterbodies.pack()

    def updateTree(self):
        """
        Updates the Data within the Tree
        """
        with open("FishPresent.txt", 'r') as file:
            json_dict = "\n".join(file.readlines()[1:])
            jsonparse = json.loads(json_dict)
            for record in self.tree.get_children():
                self.tree.delete(record)
            for location in jsonparse:
                for specie in jsonparse[location]:
                    self.tree.insert(parent='', index='end', text='',
                                     values=(specie, jsonparse[location][specie]["Number_of_Fish_Stocked"]))

    def get_direction(self):
        with open("FishPresent.txt", "r") as file:
            json_file = file.readlines()[:1]
            print(json_file)
            address = json_file[0].split("\n")
            print(address)
        Closest.getDirection(address)

class stat_page(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Ontario Fish Stocking Stats", font=title_font)
        label2 = ttk.Label(self, text="Coming Soon", font=title_font)

        label.pack(pady=10, padx=10)
        option1 = ttk.Button(self, text="Return to Menu",
                             command=lambda: controller.show_frame(main_menu))
        label2.pack()
        option1.pack()


gui = FishStockerGui()
gui.mainloop()

