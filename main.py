from tkinter import Tk, END, Text, Label, Frame, LabelFrame, Toplevel, IntVar, Checkbutton, Menu, StringVar, Button
from tkinter.ttk import Entry, Style, Combobox, OptionMenu
from variables import *
import os
from folder import get_docker_compose_file, delete_docker_compose_file, open_docker_folder, create_configuration, \
    create_directory
import subprocess
import webbrowser
from tkcalendar import Calendar
import datetime
import tkinter.messagebox as messagebox
import docker
import babel.numbers  # do not delete!
import shutil

# List of my strategy names
strategy_list = []
# Dictionary with my strategy file names as key and my strategy file path as value
strategy_file_dist = {}


def get_stock_data():
    """
    Get quotes data from the stock exchange
    :return:
    """
    # Run the docker-compose command and capture the output
    # print(print(value_rip_menu.get()))
    result = subprocess.run(
        ["docker-compose", "run", "--rm", "freqtrade", "download-data", "--exchange", "binance", "-t",
         f"{value_rip_menu.get()}",
         f"--timerange={value_date.get()}-"], stdout=subprocess.PIPE)

    # Print the output
    print(result.stdout.decode())
    print("Stock data dowloaded")
    # print(type(entry_date.get()))


def open_link(event):
    # freqtrade UI link
    webbrowser.open(url)


def open_link0(event):
    # freqtrade-strategies github link
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
    Docker compose UP command
    :return:
    """
    try:
        subprocess.run(['docker-compose', 'up', '-d'])
        print("Docker compose is started!")
        freqtrade_run.set(check_freqtrade_docker())
        docker_run.set(docker_version())
    except(Exception) as e:
        print(e)


def docker_compose_down():
    """
    Docker compose DOWN command
    :return:
    """
    try:
        subprocess.run(['docker-compose', 'down'])
        print("Docker compose is stopped!")
        freqtrade_run.set(check_freqtrade_docker())
        docker_run.set(docker_version())
    except(Exception) as e:
        print(e)


def open_config_file(lin):
    """
    Open config file in VSCode
    :param lin:
    :return:
    """
    print(strategy_file_dist.values())
    subprocess.run(['code', lin], shell=True)


# def is_numeric(string: str):
#     """
#     The function checks if the string is numeric characters.
#     :param string: The string to validate entered by the user.
#     :return: True or False
#     """
#     return string.isnumeric()


def open_setup_window(*event):
    """
    New window creation - Calendar
    :return:
    """
    # global frame_setup
    # Create the new window
    new_window = Toplevel(root)
    # new_window.geometry(setup_window_geometry)
    new_window.title("Setup - NH admin tool")
    # frame_setup = Frame(new_window)
    # # frame_setup.grid(row=0, column=0, columnspan=3, sticky="w", pady=10, padx=10)
    new_window.geometry("400x400")

    def grad_date():
        """
        Calendar date reformat
        :return: correct date
        """
        user_date = cal.get_date().split('/')
        date1 = '20' + user_date[2] + (user_date[0] if int(user_date[0]) >= 10 else "0" + user_date[0]) + \
                (user_date[1] if int(user_date[1]) >= 10 else "0" + user_date[1])
        print(date1)
        insert_value(date1)
        new_window.destroy()
        return date1

    # Setup default date
    today = datetime.date.today()
    cal = Calendar(new_window, selectmode='day', year=today.year, month=today.month, day=today.day)
    lb = Label(new_window, text="grad_date")

    cal.pack(pady=20)
    lb.pack(pady=20)

    # date.config(text="Selected Date is: " + date1)

    # Add Button and Label
    Button(new_window, text="Get Date",
           command=grad_date).pack(pady=20)

    date = Label(new_window, text="")
    date.pack(pady=20)


def insert_value(value):
    """
    Insert date to entry
    :param value:
    :return:
    """
    entry_date.delete(0, 'end')
    entry_date.insert(0, value)


def get_my_strategies():
    """
    Get list of my strategy names
    :return:
    """
    # Get the list of files in the directory
    files = os.listdir(r'C:\ft_userdata\user_data\strategies')
    # Print the list of files with their full paths
    for file in files:
        file_path = os.path.join(r'C:\ft_userdata\user_data\strategies', file)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Search for the string that starts with "class"
        for line in lines:
            if line.startswith('class'):
                strategy_list.append(line.split()[1].split('(')[0])


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


def get_value():
    """
    Get strategy file full path
    :return:
    """
    value = strategy_file_dist[selected_key.get()]
    open_config_file(value)
    print(value)


def docker_version():
    """
    Docker is working?
    :return:
    """
    # pip install docker
    # Create a Docker client
    client = docker.from_env()
    # Check if Docker is running
    if client.ping():
        print("Docker is running")
        return "Docker is running"
    else:
        print("Docker is not running")
        return "Docker is not running"


def backtesting():
    """
    Run backtesting command
    :return:
    """
    # Define the command
    command = f"docker-compose run --rm freqtrade backtesting --datadir user_data/data/binance --export trades " \
              f"--stake-amount {value_amount.get()} --strategy {combobox_strategies.get()} -i {value_rip_menu.get()} " \
              f"--timerange={value_date.get()}-"
    print(combobox_strategies.get())
    # Run the command as a subprocess
    subprocess.run(command, shell=True)


def update_docker_compose_file(file):
    """
    Update docker-compose if I want to change a Strategy
    :param file:
    :return:
    """
    print(file)
    with open("C:\\ft_userdata\\docker-compose.yml", "r") as f:
        # Read the contents of the file into a list
        lines = f.readlines()

    # Replace the 28th element in the list with "29 row"
    lines[27] = f'      --strategy {file}\n'

    # Write the modified list to the file
    with open("C:\\ft_userdata\\docker-compose.yml", "w") as f:
        f.writelines(lines)
    restart_freqtrade()


def restart_freqtrade():
    """
    Command, that restart working docker-compose
    :return:
    """
    print("start restart")
    subprocess.run(["docker-compose", "restart", "freqtrade"])
    print("finish restart")


def check_freqtrade_docker():
    try:
        output = subprocess.run(['docker', 'ps'], check=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        if 'freqtrade' in output:
            # print("freqtrade is running")
            return "freqtrade is running"
        else:
            # print("freqtrade isn't running")
            return "freqtrade isn't running"
    except subprocess.CalledProcessError:
        return False


def hyperopt():
    command = f"docker-compose run --rm freqtrade hyperopt --enable-protections --strategy {selected_strategy.get()} --hyperopt-loss SharpeHyperOptLoss -i {value_rip_menu.get()} -e {value_epoch.get()}"

    subprocess.run(command, shell=True)


def add_strategy(name):
    if os.path.exists(folder_path + "/user_data/strategies/" + name + ".py"):
        # File exists
        print("File exists")
    else:
        # File does not exist
        shutil.copy(link_strategy, folder_path + "/user_data/strategies/" + name + ".py")
        # get_my_strategies()
        # get_my_strategies_dict()
        print(f"Стратегия {name} создана!")

        with open(folder_path + "/user_data/strategies/" + name + ".py", 'r') as f:
            lines = f.readlines()

        lines[19] = f'class {name}(IStrategy):\n'

        with open(folder_path + "/user_data/strategies/" + name + ".py", 'w') as f:
            f.writelines(lines)


def delete_item(name):
    # Delete the selected item from the ComboBox

    file_path = folder_path + "/user_data/strategies/" + name
    print(file_path)
    os.remove(file_path)


# def delete_strategy():
#     pass

root = Tk()
root.geometry(main_window_geometry)
root.resizable(width=False, height=False)
root.title(title)

# Frames
frame_keepass = LabelFrame(root, text="Docker operations")
frame_keepass.grid(row=0, column=0)
try:
    main_dir_creation()
    get_my_strategies()
    get_my_strategies_dict()
except:
    print("Something wrong")
# Change directory
os.chdir('C:\\ft_userdata')

# Variables
version_var = StringVar(root)
value_rip_menu = StringVar(root)
value_date = StringVar(root)
value_amount = StringVar(root)
selected_strategy = StringVar(root)
selected_key = StringVar(root)
docker_run = StringVar(root)
freqtrade_run = StringVar(root)
value_strategy = StringVar(root)
value_epoch = StringVar(root)
value_new_name = StringVar(root)
# version_var.set(my_version())

docker_run.set(docker_version())
freqtrade_run.set(check_freqtrade_docker())

try:
    selected_strategy.set(strategy_list[0])
except:
    print("Error1")

option_menu = OptionMenu(root, selected_strategy, *strategy_list)

# Entries
entry_date = Entry(root, textvariable=value_date)
entry_date_backtesting = Entry(root, textvariable=value_date)
entry_amount_backtesting = Entry(root, textvariable=value_amount)
entry_hyperopt_epoch = Entry(root, textvariable=value_epoch)
entry_new_strategy_name = Entry(root, textvariable=value_new_name)

# Buttons
button_create_docker_compose = Button(root, text=button_text_create, command=get_docker_compose_file)
button_delete_docker_compose = Button(root, text=button_text_delete, command=delete_docker_compose_file)
button_open_docker_folder = Button(root, text=button_test_open_folder, command=open_docker_folder)
button_docker_compose_up = Button(root, text=button_text_compose_up, command=docker_compose_up)
button_docker_compose_down = Button(root, text=button_text_compose_down, command=docker_compose_down)
button_default_configs = Button(root, text=button_default_configs, command=create_configuration)
button_reset_all = Button(root, text=button_reset_all, command=create_directory)
button_open_config = Button(root, text=button_text_config_file, command=lambda: open_config_file(link_config))
button_open_strategy = Button(root, text=button_text_sample_strategy, command=lambda: open_config_file(link_strategy))
button_get_data = Button(root, text=button_text_get_data, command=get_stock_data)
button_date_from = Button(root, text=button_text_date, command=open_setup_window)
button_test = Button(root, text=button_text_open_strategy, command=get_value)
button_backtesting = Button(root, text=button_text_backtest, command=backtesting)
button_replace_docker = Button(root, text=button_text_replace_docker,
                               command=lambda: update_docker_compose_file(combobox_strategies.get()))
button_restart = Button(root, text=button_text_restart_docker, command=restart_freqtrade)
button_date_backtest = Button(root, text=button_text_date, command=open_setup_window)
button_hyperopt = Button(root, text="Hyperopt", command=hyperopt)
button_add_new_strategy = Button(root, text="Add new strategy",
                                 command=lambda: add_strategy(entry_new_strategy_name.get()))
button_delete_strategy = Button(root, text="Delete strategy", command=lambda: delete_item(selected_key.get()),
                                background='#f28174')

# Labels
label_url = Label(root, text=button_text_freqtrade_ui, fg='blue', cursor='hand2')
label_url_strategies = Label(root, text=button_text_freqtrade_strategy, fg='blue', cursor='hand2')
# label_date = Label(root, text="Date from (20221023):")
label_version = Label(root, textvariable=version_var)
label_docker = Label(root, textvariable=docker_run)
label_freqtrade = Label(root, textvariable=freqtrade_run)

# Comboboxes
combo = Combobox(root, textvariable=value_rip_menu, values=timeframes)
combobox_strategies = Combobox(root, textvariable=selected_strategy, values=strategy_list)
combobox_keys = Combobox(root, textvariable=selected_key, values=list(strategy_file_dist.keys()))
combo_strategy = Combobox(root, textvariable=value_rip_menu, values=timeframes)
combobox_strategies_hyperopt = Combobox(root, textvariable=selected_strategy, values=strategy_list)
combo_strategy_hyperopt = Combobox(root, textvariable=value_rip_menu, values=timeframes)

# my_version()

# ROW 0
button_create_docker_compose.grid(row=0, column=0)
button_delete_docker_compose.grid(row=0, column=1)
button_open_docker_folder.grid(row=0, column=2)
# label_version.grid(row=0, column=3)
label_docker.grid(row=0, column=3)
label_freqtrade.grid(row=0, column=4)

# ROW 1
button_docker_compose_up.grid(row=1, column=0)
button_docker_compose_down.grid(row=1, column=1)
button_default_configs.grid(row=1, column=2)
button_reset_all.grid(row=1, column=3)

# ROW 2
label_url.grid(row=2, column=0)
button_open_config.grid(row=2, column=1)
button_open_strategy.grid(row=2, column=2)
label_url_strategies.grid(row=2, column=3)

# label_date.grid(row=3, column=0)

# ROW 3
entry_date.grid(row=3, column=0)
button_date_from.grid(row=3, column=1)
combo.grid(row=3, column=2)
button_get_data.grid(row=3, column=3)
entry_date_backtesting.insert(END, button_text_date)

# ROW 4
combobox_keys.grid(row=4, column=0)
button_test.grid(row=4, column=1)
button_delete_strategy.grid(row=4, column=2)
entry_new_strategy_name.grid(row=4, column=3)
button_add_new_strategy.grid(row=4, column=4)

# ROW 5
combobox_strategies.grid(row=5, column=0)
entry_date_backtesting.grid(row=5, column=1)
button_date_backtest.grid(row=5, column=2)
combo_strategy.grid(row=5, column=3)
entry_amount_backtesting.grid(row=5, column=4)
button_backtesting.grid(row=5, column=5)
entry_amount_backtesting.insert(END, '700')

# ROW 6
button_replace_docker.grid(row=6, column=0)
button_restart.grid(row=6, column=1)

# ROW 7
combobox_strategies_hyperopt.grid(row=7, column=0)
combo_strategy_hyperopt.grid(row=7, column=1)
entry_hyperopt_epoch.grid(row=7, column=2)
button_hyperopt.grid(row=7, column=3)
entry_hyperopt_epoch.insert(END, 'Epoch int value')

label_url.bind('<1>', open_link)
label_url_strategies.bind('<1>', open_link0)

root.mainloop()
