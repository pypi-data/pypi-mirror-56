import os
from termcolor_util import cyan

from project_archer.environment.read_shell_parameters import project_folder
from project_archer.storage.project_data import read_project_yml

def list_projects(args, env):
    folder = project_folder(args)

    env.log("Available projects:")

    items = list(sorted(os.listdir(folder)))

    for filename in items:
        if not os.path.isfile(os.path.join(folder, filename)):
            continue

        file_data = open(os.path.join(folder, filename))
        project_data = read_project_yml(file_data)
        env.log(" - " + cyan(os.path.splitext(filename)[0], bold=True) + ": " + project_data['name'])
