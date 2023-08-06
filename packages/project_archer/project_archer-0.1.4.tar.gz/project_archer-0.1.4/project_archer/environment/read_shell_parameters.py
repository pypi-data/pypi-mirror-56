import argparse

parser = argparse.ArgumentParser()
parser.add_argument('project', nargs='?', metavar="PROJECT",
    help="switch current project to PROJECT, or if -e, edit PROJECT")
parser.add_argument('-n', '--new', metavar="PROJECT",
    help="create a new project")
parser.add_argument('-e', '--edit', action='store_true',
    help="edit the given project, or the current project")
parser.add_argument('--layout', action='store_true',
    help="specify that we want to use the layouts")
parser.add_argument('--internalRunMode', required=True, metavar="MODE",
    help="specify the internal command that is used (e.g. project, server, etc.)")
parser.add_argument('-l', '--list', action='store_true',
    help="list the available projects")

import os, os.path

def current_project(run_mode):
    return os.getenv("CIPLOGIC_ARCHER_CURRENT_" + run_mode.upper())

def archer_home(subpath):
    if 'ARCHER_HOME' in os.environ:
        path = os.environ['ARCHER_HOME']
    else:
        path = os.path.join(os.environ['HOME'], ".archer")

    path = os.path.normpath(path)

    if subpath:
        return os.path.join(path, subpath)
    else:
        return path

def project_folder(args):
    if args.layout:
        return archer_home(args.internalRunMode + "s/layouts")
    else:
        return archer_home(args.internalRunMode + "s")
