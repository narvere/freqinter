import subprocess
import os

# subprocess.run(["code", "C:/ft_userdata/user_data/config.json"])
files = os.listdir()
for file in files:
    print(file)

subprocess.run(['code', "C:/ft_userdata/user_data/config.json"], shell=True)

