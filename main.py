from tkinter import Tk, END, Text, Label, Frame, LabelFrame, Toplevel, IntVar, Checkbutton, Menu
from tkinter.ttk import Entry, Button, Style
from variables import *
import os
from folder import get_docker_compose_file, delete_docker_compose_file


def main_dir_creation():
    """
    Create work dir if not exist
    :return:
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


root = Tk()
root.geometry(main_window_geometry)
root.resizable(width=False, height=False)
root.title(title)

main_dir_creation()

# Change directory
os.chdir('C:\\ft_userdata')

button_create_docker_compose = Button(root, text="Create docker-compose", command=get_docker_compose_file)
button_delete_docker_compose = Button(root, text="Delete docker-compose", command=delete_docker_compose_file)
button_create_docker_compose.grid(row=0, column=0)
button_delete_docker_compose.grid(row=0, column=1)

root.mainloop()
