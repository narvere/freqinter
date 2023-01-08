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

# pip install tkinter-tooltip

# List of my strategy names
strategy_list = []
# Dictionary with my strategy file names as key and my strategy file path as value
strategy_file_dist = {}


# test
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


docker_condition = False


def docker_version():
    global docker_condition
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
        docker_condition = True
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


freqtrade_condition = False


def check_freqtrade_docker():
    global freqtrade_condition
    try:
        output = subprocess.run(['docker', 'ps'], check=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        if 'freqtrade' in output:
            # print("freqtrade is running")
            freqtrade_condition = True
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
        # combobox_keys.insert(name)


def delete_item(name):
    # Delete the selected item from the ComboBox

    file_path = folder_path + "/user_data/strategies/" + name
    os.remove(file_path)
    # print(name)
    # print(file_path, "Deleted")


keys = list(strategy_file_dist.keys())


def delete_file(name):
    # Delete the selected item from the ComboBox

    file_path = folder_path + "/user_data/strategies/" + name
    os.remove(file_path)





def delete_strategy():
    # Get the currently selected item from the combobox
    current_item = combobox_keys.get()
    # combobox_keys.delete(current_item)

    # Remove the item from the list of keys
    keys.remove(current_item)

    # Remove strategy file from working directory
    delete_file(current_item)

    # Remove the key-value pair from the dictionary
    del strategy_file_dist[current_item]

    # Update the values in the combobox
    combobox_keys["values"] = keys


# def delete_strategy():
#     pass

root = Tk()
root.geometry(main_window_geometry)
root.resizable(width=False, height=False)
root.title(title)

# Frames
frame_docker = LabelFrame(root, text="Docker operations")
frame_config = LabelFrame(root, text="Config zone")
frame_stock_data = LabelFrame(root, text="Stock data")
frame_my_srategies = LabelFrame(root, text="My strategies")
frame_backtest = LabelFrame(root, text="Backtest")
frame_hyperopt = LabelFrame(root, text="Hyperopt")

frame_docker.grid(row=0, column=0, columnspan=3, padx=10, pady=5, rowspan=2)
frame_config.grid(row=2, column=0, columnspan=3, padx=10)
frame_stock_data.grid(row=3, column=0, columnspan=3, padx=10)
frame_my_srategies.grid(row=4, column=0, columnspan=5, padx=10, sticky="w")
frame_backtest.grid(row=5, column=0, rowspan=2, columnspan=5, padx=10, sticky="w")
frame_hyperopt.grid(row=7, column=0, columnspan=3, padx=10)

frame_docker_min_columnsize = 172
frame_docker.grid_columnconfigure(0, minsize=frame_docker_min_columnsize)
frame_docker.grid_columnconfigure(1, minsize=frame_docker_min_columnsize)
frame_docker.grid_columnconfigure(2, minsize=frame_docker_min_columnsize)
frame_docker.grid_columnconfigure(3, minsize=frame_docker_min_columnsize)
frame_config.grid_columnconfigure(0, minsize=frame_docker_min_columnsize)
frame_config.grid_columnconfigure(1, minsize=frame_docker_min_columnsize)
frame_config.grid_columnconfigure(2, minsize=frame_docker_min_columnsize)
frame_config.grid_columnconfigure(3, minsize=frame_docker_min_columnsize)
frame_stock_data.grid_columnconfigure(0, minsize=frame_docker_min_columnsize)
frame_stock_data.grid_columnconfigure(1, minsize=frame_docker_min_columnsize)
frame_stock_data.grid_columnconfigure(2, minsize=frame_docker_min_columnsize)
frame_stock_data.grid_columnconfigure(3, minsize=frame_docker_min_columnsize)
frame_my_srategies.grid_columnconfigure(0, minsize=frame_docker_min_columnsize)
frame_my_srategies.grid_columnconfigure(1, minsize=100)
frame_my_srategies.grid_columnconfigure(2, minsize=135)
frame_my_srategies.grid_columnconfigure(3, minsize=frame_docker_min_columnsize)
frame_backtest.grid_columnconfigure(0, minsize=158)
frame_backtest.grid_columnconfigure(1, minsize=158)
frame_backtest.grid_columnconfigure(2, minsize=158)
frame_backtest.grid_columnconfigure(3, minsize=150)
frame_hyperopt.grid_columnconfigure(0, minsize=frame_docker_min_columnsize)
frame_hyperopt.grid_columnconfigure(1, minsize=frame_docker_min_columnsize)
frame_hyperopt.grid_columnconfigure(2, minsize=frame_docker_min_columnsize)
frame_hyperopt.grid_columnconfigure(3, minsize=frame_docker_min_columnsize)
# frame_backtest.grid_columnconfigure(4, minsize=frame_docker_min_columnsize)
# frame_docker.grid_columnconfigure(4, minsize=frame_docker_min_columnsize)
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
entry_date = Entry(frame_stock_data, textvariable=value_date)
entry_date_backtesting = Entry(frame_backtest, textvariable=value_date)
entry_amount_backtesting = Entry(frame_backtest, textvariable=value_amount)
entry_hyperopt_epoch = Entry(frame_hyperopt, textvariable=value_epoch)
entry_new_strategy_name = Entry(frame_my_srategies, textvariable=value_new_name)

# Buttons
button_create_docker_compose = Button(frame_docker, text=button_text_create, command=get_docker_compose_file)
button_delete_docker_compose = Button(frame_docker, text=button_text_delete, command=delete_docker_compose_file)
button_open_docker_folder = Button(frame_docker, text=button_test_open_folder, command=open_docker_folder)
button_docker_compose_up = Button(frame_docker, text=button_text_compose_up, command=docker_compose_up)
button_docker_compose_down = Button(frame_docker, text=button_text_compose_down, command=docker_compose_down)
button_default_configs = Button(frame_docker, text=button_default_configs, command=create_configuration,
                                background='#92f095')
button_reset_all = Button(frame_docker, text=button_reset_all, command=create_directory, background='#f28174')
button_restart = Button(frame_docker, text=button_text_restart_docker, command=restart_freqtrade)

button_open_config = Button(frame_config, text=button_text_config_file, command=lambda: open_config_file(link_config))
button_open_strategy = Button(frame_config, text=button_text_sample_strategy,
                              command=lambda: open_config_file(link_strategy))
button_get_data = Button(frame_stock_data, text=button_text_get_data, command=get_stock_data)
button_date_from = Button(frame_stock_data, text=button_text_date, command=open_setup_window)
button_test = Button(frame_my_srategies, text=button_text_open_strategy, command=get_value)
button_backtesting = Button(frame_backtest, text=button_text_backtest, command=backtesting)
button_replace_docker = Button(frame_backtest, text=button_text_replace_docker,
                               command=lambda: update_docker_compose_file(combobox_strategies.get()))

button_date_backtest = Button(frame_backtest, text=button_text_date, command=open_setup_window)
button_hyperopt = Button(frame_hyperopt, text="Hyperopt", command=hyperopt)
button_add_new_strategy = Button(frame_my_srategies, text=button_text_add_atrategy,
                                 command=lambda: add_strategy(entry_new_strategy_name.get()))
button_delete_strategy = Button(frame_my_srategies, text=button_test_del_strategy,
                                command=delete_strategy,
                                background='#f28174')

# Labels
label_url = Label(frame_config, text=button_text_freqtrade_ui, fg='blue', cursor='hand2')
label_url_strategies = Label(frame_config, text=button_text_freqtrade_strategy, fg='blue', cursor='hand2')
# label_date = Label(root, text="Date from (20221023):")
label_version = Label(root, textvariable=version_var)
if docker_condition:
    label_docker = Label(frame_backtest, textvariable=docker_run, fg="green", font=['Arial', 10, 'bold'])
else:
    label_docker = Label(frame_backtest, textvariable=docker_run, fg="red", font=['Arial', 10, 'bold'])

if freqtrade_condition:
    label_freqtrade = Label(frame_backtest, textvariable=freqtrade_run, fg="green", font=['Arial', 10, 'bold'])
else:
    label_freqtrade = Label(frame_backtest, textvariable=freqtrade_run, fg="red", font=['Arial', 10, 'bold'])

get_my_strategies_dict()
keys = list(strategy_file_dist.keys())
# Comboboxes
combo = Combobox(frame_stock_data, textvariable=value_rip_menu, values=timeframes)
combobox_strategies = Combobox(frame_backtest, textvariable=selected_strategy, values=strategy_list)
combobox_keys = Combobox(frame_my_srategies, textvariable=selected_key, values=keys)
combo_strategy = Combobox(frame_backtest, textvariable=value_rip_menu, values=timeframes)
combobox_strategies_hyperopt = Combobox(frame_hyperopt, textvariable=selected_strategy, values=strategy_list)
combo_strategy_hyperopt = Combobox(frame_hyperopt, textvariable=value_rip_menu, values=timeframes)
combobox_keys.set("Choose an item")
# my_version()
# Frame Docker operations
# ROW 0
button_create_docker_compose.grid(row=0, column=0, sticky="we", padx=3, pady=3)
button_delete_docker_compose.grid(row=0, column=1, sticky="we", padx=3, pady=3)
button_open_docker_folder.grid(row=0, column=2, sticky="we", padx=3, pady=3)
button_reset_all.grid(row=0, column=3, sticky="we", padx=3, pady=3)
# label_version.grid(row=0, column=3)

# ROW 1
button_docker_compose_up.grid(row=1, column=0, sticky="we", padx=3, pady=3)
button_docker_compose_down.grid(row=1, column=1, sticky="we", padx=3, pady=3)
button_restart.grid(row=1, column=2, sticky="we", padx=3, pady=3)
button_default_configs.grid(row=1, column=3, sticky="we", padx=3, pady=3)

label_docker.grid(row=0, column=2)
label_freqtrade.grid(row=0, column=3)

# Frame Config zone
# ROW 2
label_url.grid(row=0, column=0, sticky="we", padx=3, pady=3)
label_url_strategies.grid(row=0, column=1, sticky="we", padx=3, pady=3)
button_open_config.grid(row=0, column=2, sticky="we", padx=3, pady=3)
button_open_strategy.grid(row=0, column=3, sticky="we", padx=3, pady=3)

# label_date.grid(row=3, column=0)

# Frame Stock data
# ROW 3
entry_date.grid(row=0, column=0, sticky="we", padx=3)
button_date_from.grid(row=0, column=1, sticky="w", padx=3, pady=3)
combo.grid(row=0, column=2, sticky="we", padx=3)
button_get_data.grid(row=0, column=3, sticky="w", padx=3, pady=3)
entry_date_backtesting.insert(END, button_text_date)

# Frame My strategies
# ROW 4
combobox_keys.grid(row=0, column=0, sticky="we", padx=3)
button_test.grid(row=0, column=1, sticky="w", padx=3)
button_delete_strategy.grid(row=0, column=2, padx=3)
entry_new_strategy_name.grid(row=0, column=3, sticky="we", padx=3)
button_add_new_strategy.grid(row=0, column=4, sticky="w", padx=3)

# Frame Backtest
# ROW 5
combobox_strategies.grid(row=0, column=0, padx=3, pady=3, sticky="we")
button_replace_docker.grid(row=0, column=1, padx=3, pady=3)
label_url.bind('<1>', open_link)
label_url_strategies.bind('<1>', open_link0)

# ROW 6
entry_date_backtesting.grid(row=1, column=0, padx=3, pady=3, sticky="we")
button_date_backtest.grid(row=1, column=1, padx=3, pady=3, sticky="w")
combo_strategy.grid(row=1, column=2, padx=3, pady=3, sticky="we")
entry_amount_backtesting.grid(row=1, column=3, padx=3, pady=3, sticky="we")
button_backtesting.grid(row=1, column=4, padx=3, pady=3, sticky="w")
entry_amount_backtesting.insert(END, '700')
combo_strategy.insert(END, 'Timeframe')

# Frame Hyperopt
# ROW 7
combobox_strategies_hyperopt.grid(row=0, column=0, padx=3, pady=3, sticky="we")
combo_strategy_hyperopt.grid(row=0, column=1, padx=3, pady=3, sticky="we")
entry_hyperopt_epoch.grid(row=0, column=2, padx=3, pady=3, sticky="we")
button_hyperopt.grid(row=0, column=3, padx=3, pady=3, sticky="we")
entry_hyperopt_epoch.insert(END, 'Epoch int value')

root.mainloop()
