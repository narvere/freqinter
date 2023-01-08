import tkinter as tk
from tkinter.ttk import Entry, Style, Combobox

# Create the main window
window = tk.Tk()

# Create a list of items for the combobox
items = ["item1", "item2", "item3"]

# Create the combobox
combobox = tk.ttk.Combobox(window, values=items)


# Create a function that will be called when the button is clicked
def delete_item():
    # Get the currently selected item from the combobox
    current_item = combobox.get()

    # Remove the item from the list of items
    items.remove(current_item)

    # Update the values in the combobox
    combobox["values"] = items


# Create the button
button = tk.Button(window, text="Delete Item", command=delete_item)

# Pack the combobox and button to the window
combobox.pack()
button.pack()

# Run the main loop
window.mainloop()
