from tkinter import Tk, END, Text, Label, Frame, LabelFrame, Toplevel, IntVar, Checkbutton, Menu, StringVar
from tkinter.ttk import Entry, Button, Style
from variables import *
import os
from folder import get_docker_compose_file, delete_docker_compose_file, open_docker_folder, create_configuration, \
    create_directory
import subprocess
import webbrowser


def open_link(event):
    webbrowser.open('http://127.0.0.1:8080/')


def main_dir_creation():
    """
    Create work dir if not exist
    :return:
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def my_version():
    """
    Getting installed Freqtrade version
    :return:
    """
    version = subprocess.run(
        ['docker-compose', 'run', '--rm', 'freqtrade', '--version'],
        stdout=subprocess.PIPE)
    return f"Ver: {version.stdout.decode()}"


def docker_compose_up():
    """
    Docker compose UP
    :return:
    """
    try:
        subprocess.run(['docker-compose', 'up', '-d'])
        print("Docker compose is started!")
    except(Exception) as e:
        print(e)


def docker_compose_down():
    """
    Docker compose down
    :return:
    """
    try:
        subprocess.run(['docker-compose', 'down'])
        print("Docker compose is stopped!")
    except(Exception) as e:
        print(e)


root = Tk()
root.geometry(main_window_geometry)
root.resizable(width=False, height=False)
root.title(title)

main_dir_creation()

# Change directory
os.chdir('C:\\ft_userdata')

# Version variable creation
version_var = StringVar()
version_var.set(my_version())

button_create_docker_compose = Button(root, text=button_text_create, command=get_docker_compose_file)
button_delete_docker_compose = Button(root, text=button_text_delete, command=delete_docker_compose_file)
button_open_docker_folder = Button(root, text=button_test_open_folder, command=open_docker_folder)
button_docker_compose_up = Button(root, text=button_text_compose_up, command=docker_compose_up)
button_docker_compose_down = Button(root, text=button_text_compose_down, command=docker_compose_down)
button_default_configs = Button(root, text=button_default_configs, command=create_configuration)
button_reset_all = Button(root, text=button_reset_all, command=create_directory)
label_url = Label(root, text='Freqtrade UI', fg='blue', cursor='hand2')

label_version = Label(root, textvariable=version_var)
my_version()
button_create_docker_compose.grid(row=0, column=0)
button_delete_docker_compose.grid(row=0, column=1)
button_open_docker_folder.grid(row=0, column=2)
label_version.grid(row=0, column=3)
button_docker_compose_up.grid(row=1, column=0)
button_docker_compose_down.grid(row=1, column=1)
button_default_configs.grid(row=1, column=2)
button_reset_all.grid(row=1, column=3)


label_url.grid(row=2, column=0)
label_url.bind('<1>', open_link)

root.mainloop()
