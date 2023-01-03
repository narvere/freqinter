import subprocess
import os
from variables import *
import shutil

# Change directory
os.chdir(work_directory)

full_path = f'{work_directory} docker-compose.yml'
full_path_upd = f'{work_directory}docker-compose.yml'


def remove_space_from_filename():
    """
    Remove space from file docker-compose
    :return:
    """
    global new_path
    print(full_path)
    try:
        x = full_path.split('\\')[:-1]
        x.append(full_path.split('\\')[-1].strip())
        new_path = '\\'.join(x)
        os.rename(full_path, new_path)
    except(Exception):
        print("Docker-compose exist!")

# files = os.listdir()
# for file in files:
#     print(file)

def pull_image():
    """
    Pull the freqtrade image
    :return:
    """
    global new_path
    new_path = subprocess.run(['docker-compose', 'pull'], stdout=subprocess.PIPE)
    print(new_path.stdout.decode())


def create_directory():
    """
    Create user directory structure
    :return:
    """
    new_path2 = subprocess.run(
        ['docker-compose', 'run', '--rm', 'freqtrade', 'create-userdir', '--userdir', 'user_data'],
        stdout=subprocess.PIPE)
    print(new_path2.stdout.decode())
    print("Directory structure created!")


def create_configuration():
    """
    Create configuration - Requires answering interactive questions
    :return:
    """
    subprocess.run(['docker-compose', 'run', '--rm', 'freqtrade', 'new-config', '--config', 'user_data/config.json'])
    print("Default configuration created!")
    # print(config.stdout.decode())


def get_docker_compose_file():
    """
    Download the docker-compose file from the repository
    :return:
    """
    if not os.path.exists(full_path):
        result = subprocess.run(
            ['curl', docker_compose_url, '-o docker-compose.yml'], stdout=subprocess.PIPE)
        print(result.stdout.decode())
        remove_space_from_filename()
        pull_image()
        # create_directory()
        # create_configuration()
        print("Freqtrade installed!")
    else:
        print("docker-compose is exist")


# get_docker_compose_file()


def delete_docker_compose_file():
    """
    Function delete all docker-compose files in a dir.
    :return:
    """
    for file in os.listdir(work_directory):
        file_path = os.path.join(work_directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
        # Delete not empty folder
        shutil.rmtree(work_directory)


def open_docker_folder():
    """
    Open working dir
    :return:
    """
    subprocess.run(['explorer', work_directory])
