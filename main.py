from tkinter import Tk, END, Text, Label, Frame, LabelFrame, Toplevel, IntVar, Checkbutton, Menu, StringVar
from tkinter.ttk import Entry, Button, Style, Combobox
from variables import *
import os
from folder import get_docker_compose_file, delete_docker_compose_file, open_docker_folder, create_configuration, \
    create_directory
import subprocess
import webbrowser


def get_stock_data():
    # Run the docker-compose command and capture the output
    print(value_rip_menu.get())
    result = subprocess.run(
        ["docker-compose", "run", "--rm", "freqtrade", "download-data", "--exchange", "binance", "-t", f"{value_rip_menu.get()}",
         "--timerange=20221110-"], stdout=subprocess.PIPE)

    # Print the output
    print(result.stdout.decode())
    print("Stock data dowloaded")
    print(entry_date.get())


def open_link(event):
    webbrowser.open(url)


def open_link0(event):
    webbrowser.open(url2)


def main_dir_creation():
    """
    Create work dir if not exist
    :return:
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Working directory is created!")


def my_version():
    """
    Getting installed Freqtrade version
    :return:
    """
    version = subprocess.run(
        ['docker-compose', 'run', '--rm', 'freqtrade', '--version'],
        stdout=subprocess.PIPE)
    print(version.stdout.decode() + "1")
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


def open_config_file(lin):
    subprocess.run(['code', lin], shell=True)


root = Tk()
root.geometry(main_window_geometry)
root.resizable(width=False, height=False)
root.title(title)

main_dir_creation()

# Change directory
os.chdir('C:\\ft_userdata')

# Version variable creation
version_var = StringVar()
value_rip_menu = StringVar()
version_var.set(my_version())

entry_date = Entry(root)

button_create_docker_compose = Button(root, text=button_text_create, command=get_docker_compose_file)
button_delete_docker_compose = Button(root, text=button_text_delete, command=delete_docker_compose_file)
button_open_docker_folder = Button(root, text=button_test_open_folder, command=open_docker_folder)
button_docker_compose_up = Button(root, text=button_text_compose_up, command=docker_compose_up)
button_docker_compose_down = Button(root, text=button_text_compose_down, command=docker_compose_down)
button_default_configs = Button(root, text=button_default_configs, command=create_configuration)
button_reset_all = Button(root, text=button_reset_all, command=create_directory)
button_open_config = Button(root, text="Open config file", command=lambda: open_config_file(link_config))
button_open_strategy = Button(root, text="Open sample_strategy file", command=lambda: open_config_file(link_strategy))
button_get_data = Button(root, text="Get stock data", command=get_stock_data)

label_url = Label(root, text='Freqtrade UI', fg='blue', cursor='hand2')
label_url_strategies = Label(root, text='freqtrade-strategies', fg='blue', cursor='hand2')
label_date = Label(root, text="Date from (20221023):")

label_version = Label(root, textvariable=version_var)
# my_version()
button_create_docker_compose.grid(row=0, column=0)
button_delete_docker_compose.grid(row=0, column=1)
button_open_docker_folder.grid(row=0, column=2)
label_version.grid(row=0, column=3)

button_docker_compose_up.grid(row=1, column=0)
button_docker_compose_down.grid(row=1, column=1)
button_default_configs.grid(row=1, column=2)
button_reset_all.grid(row=1, column=3)

label_url.grid(row=2, column=0)
button_open_config.grid(row=2, column=1)
button_open_strategy.grid(row=2, column=2)
label_url_strategies.grid(row=2, column=3)

combo = Combobox(root, textvariable=value_rip_menu,
                 values=['1s', '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d',
                         '1w', '1M'])
label_date.grid(row=3, column=0)
entry_date.grid(row=3, column=1)
combo.grid(row=3, column=2)
button_get_data.grid(row=3, column=3)

label_url.bind('<1>', open_link)
label_url_strategies.bind('<1>', open_link0)

root.mainloop()
