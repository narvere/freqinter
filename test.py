import shutil
from variables import link_strategy, folder_path
import os.path

name = "deniss_test1"

if os.path.exists(folder_path + "/user_data/strategies/" + name + ".py"):
    # File exists
    print("File exists")
else:
    # File does not exist
    shutil.copy(link_strategy, folder_path + "/user_data/strategies/" + name + ".py")
    print(f"Стратегия {name} создана!")

    with open(folder_path + "/user_data/strategies/" + name + ".py", 'r') as f:
        lines = f.readlines()

    lines[19] = f'class {name}(IStrategy):\n'

    with open(folder_path + "/user_data/strategies/" + name + ".py", 'w') as f:
        f.writelines(lines)
