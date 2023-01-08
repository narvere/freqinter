import tkinter as tk
from tkinter.ttk import Entry, Style, Combobox
import os
from variables import *

# Create the main window
window = tk.Tk()

# Create a dictionary
strategy_file_dist = {}


def get_my_strategies_dict():
    """
    Get dictionary of my strategy "file name: file path"
    :return:
    """
    # Get the list of files in the directory
    files = os.listdir(r'C:\ft_userdata\user_data\strategies')
    # Print the list of files with their full paths
    for file in files:
        file_path = os.path.join(r'C:\ft_userdata\user_data\strategies', file)
        name = file_path.split('\\')[-1]
        strategy_file_dist[name] = file_path
        # print(file_path.split('\\')[-1])


def delete_file(name):
    # Delete the selected item from the ComboBox

    file_path = folder_path + "/user_data/strategies/" + name
    os.remove(file_path)


get_my_strategies_dict()

# Create a list of keys for the combobox
keys = list(strategy_file_dist.keys())

# Create the combobox
combobox = Combobox(window, values=keys)


# Create a function that will be called when the button is clicked
def delete_item():
    # Get the currently selected item from the combobox
    current_item = combobox.get()

    # Remove the item from the list of keys
    keys.remove(current_item)
    delete_file(current_item)

    # Remove the key-value pair from the dictionary
    del strategy_file_dist[current_item]

    # Update the values in the combobox
    combobox["values"] = keys


# Create the button
button = tk.Button(window, text="Delete Item", command=delete_item)

# Pack the combobox and button to the window
combobox.pack()
button.pack()

# Run the main loop
window.mainloop()
