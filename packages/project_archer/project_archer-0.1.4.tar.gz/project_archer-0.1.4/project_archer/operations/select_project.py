import os

from project_archer.environment.read_shell_parameters import archer_home, current_project
from project_archer.storage.project_data import read_project_yml

def select_project(args, env):
    project_name = args.project
    project_data = read_project_data(project_name, args.internalRunMode)

    # 1. check if the project can be activated
    required_envvars = project_data['requires']
    missing_envvars = [v for v in required_envvars
        if not os.getenv(v) and v not in project_data['exports']]

    if len(missing_envvars):
        env.log("Unable to activate: " + project_name + "!");
        env.log("Missing environment variables: '" + "', '".join(missing_envvars) + "'.")
        return # bailing out

    old_project_name = current_project(args.internalRunMode)
    if (old_project_name == project_name):
        env.log("The current " + args.internalRunMode + " is already: " + project_name + ".");
        return # bailing out

    # 2. deactivate the previous project
    if (old_project_name):
        old_project = read_project_data(old_project_name, args.internalRunMode)
        execute_commands(old_project['deactivate'], env)
        unset_commands(old_project['commands'], env)
        unset_envvars(old_project['exports'], env)

    # 3. export the environment variables
    for export_name in project_data['exports']:
        env.set_envvar(export_name, project_data['exports'][export_name])

    # 4. activate the current project
    execute_commands(project_data['activate'], env)

    # 5. export the commands
    export_commands(project_data['commands'], env)

    #print(project_data['name'], project_name)
    env.log("Activated " + args.internalRunMode + ": " + project_data['name'])
    env.set_envvar("CIPLOGIC_ARCHER_CURRENT_" + args.internalRunMode.upper(),
                   project_name)

def read_project_data(project_name, internal_run_mode, projects_folder=None):
    if not projects_folder:
        projects_folder = archer_home(internal_run_mode + "s")

    project_file = os.path.join(projects_folder, project_name + ".yml")
    project_data = read_project_yml(open(project_file))

    result = {
        'name': "<none>",
        'layouts': [],
        'requires': [],
        'activate': [],
        'deactivate': [],
        'commands': {},
        'exports': {},
    }

    # this is nominally recursive - however, the |layouts| subobjects in the yml
    # files do not contain their own |layouts| entry, so this should loop should
    # not run again
    for (i, layout) in enumerate(project_data['layouts']):
        layout_data = read_project_data(layout, internal_run_mode,
            archer_home(internal_run_mode + "s/layouts"))
        mix(result, layout_data)

    result['layouts'] = project_data['layouts']
    result['name'] = project_data['name']
    mix(result, project_data)

    return result

# mutates source
def mix(source, extra):
    source['requires'].extend(extra['requires'])
    source['deactivate'][0:0] = extra['deactivate']
    source['activate'].extend(extra['activate'])

    for k in extra['commands']:
        source['commands'][k] = extra['commands'][k]
    for k in extra['exports']:
        source['exports'][k] = extra['exports'][k]

def execute_commands(commands, env):
    for command in "\n".join(commands).split('\n'):
        if command.strip(): # ignore empty commands
            env.execute(command)

def export_commands(commands, env):
    env.log("Commands: ")

    for command in commands:
        env.log("   " + command)
        env.define_command(command, commands[command])

def unset_commands(commands, env):
    for command in commands:
        env.remove_command(command)

def unset_envvars(envvars, env):
    for envvar in envvars:
        env.unset_envvar(envvar)
