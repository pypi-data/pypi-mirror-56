import boto3
import argparse
import click
import fnmatch
import json
import jsonschema
import logging
import os
import shutil
import sys
import tabulate

from ray.projects import ProjectDefinition
import ray.projects.scripts as ray_scripts
import ray.ray_constants

import anyscale.conf
from anyscale.project import (PROJECT_ID_BASENAME, get_project_id)
from anyscale.snapshot import (create_snapshot, delete_snapshot,
        describe_snapshot, download_snapshot, get_snapshot_uuid, list_snapshots)
from anyscale.util import (confirm, deserialize_datetime,
        humanize_timestamp, send_json_request)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE


def get_or_create_snapshot(snapshot_uuid, project_definition, yes, local):
    # If no snapshot was provided, create a snapshot.
    if snapshot_uuid is None:
        confirm("No snapshot specified for the command. Create a new snapshot?", yes)
        # TODO: Give the snapshot a name and description that includes this
        # session's name.
        snapshot_uuid = create_snapshot(project_definition, yes, local=True)
    else:
        snapshot_uuid = get_snapshot_uuid(project_definition.root, snapshot_uuid)
    return snapshot_uuid


def load_project_or_throw():
    try:
        project = ray.projects.ProjectDefinition(os.getcwd())
    except (jsonschema.exceptions.ValidationError, ValueError) as e:
        raise click.ClickException(e)

    dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir, "anyscale_schema.json")) as f:
        schema = json.load(f)

    # Validate the project file.
    try:
        jsonschema.validate(instance=project.config, schema=schema)
    except (jsonschema.exceptions.ValidationError, ValueError) as e:
        raise click.ClickException(e)

    return project


@click.group()
def cli():
    pass


@click.group(
    "project", help="Commands for working with projects.")
def project_cli():
    pass


@click.group(
    "session", help="Commands for working with sessions.")
def session_cli():
    pass


@click.group(
    "snapshot", help="Commands for working with snapshot.")
def snapshot_cli():
    pass


@project_cli.command(
    name="validate",
    help="Validate current project specification.")
@click.option(
    "--verbose", help="If set, print the validated file", is_flag=True)
def project_validate(verbose):
    project = load_project_or_throw()
    print("Project files validated!", file=sys.stderr)
    if verbose:
        print(project.config)


@project_cli.command(
    name="create",
    help="Create a new project within current directory. If the project name "
         "is not provided, this will register the existing project.")
@click.argument("project_name", required=False)
@click.option(
    "--cluster-yaml",
    help="Path to autoscaler yaml. Created by default",
    default=None)
@click.option(
    "--requirements",
    help="Path to requirements.txt. Created by default",
    default=None)
@click.pass_context
def project_create(ctx, project_name, cluster_yaml, requirements):
    project_id_path = os.path.join(ray_scripts.PROJECT_DIR, PROJECT_ID_BASENAME)

    if project_name:
        # Call the normal `ray project create` command.
        ctx.forward(ray_scripts.create)
    elif not os.path.exists(ray_scripts.PROJECT_DIR):
        raise click.ClickException("No registered project found. Did you "
                "forget to pass the project name to `any project create`?")

    try:
        project_definition = load_project_or_throw()
    except click.ClickException as e:
        if not project_name:
            raise click.ClickException("No registered project found. Did you "
                    "forget to pass the project name to `any project create`?")
        else:
            raise e

    project_name = project_definition.config["name"]
    # Add a description of the output_files parameter to the project yaml.
    if not "output_files" in project_definition.config:
        with open(ray_scripts.PROJECT_YAML, 'a') as f:
            f.write("\n".join([
                "",
                "# Pathnames for files and directories that should be saved in a snapshot but",
                "# that should not be synced with a session. Pathnames can be relative to the",
                "# project directory or absolute. Generally, this should be files that were",
                "# created by an active session, such as application checkpoints and logs.",
                "output_files: [",
                "  # For example, uncomment this to save the logs from the last ray job.",
                "  # \"/tmp/ray/session_latest\",",
                "]",
                ]))

    if os.path.exists(project_id_path):
        with open(project_id_path, 'r') as f:
            project_id = int(f.read())
        resp = send_json_request("project_list", {
            "project_id": project_id,
            })
        if len(resp["projects"]) == 0:
            raise click.ClickException("This project has already been "
                    "registered, but its database entry has been deleted?")
        elif len(resp["projects"]) > 1:
            raise click.ClickException("Multiple projects found with the same ID.")

        project = resp["projects"][0]
        if project_name != project["name"]:
            raise ValueError("Project name {} does not match saved project name "
                    "{}".format(project_name, project["name"]))

        raise click.ClickException("This project has already been registered")

    # Add a local database entry for the new Project.
    resp = send_json_request("project_create", {
        "project_name": project_name,
        }, post=True)
    project_id = resp["project_id"]
    with open(project_id_path, 'w+') as f:
        f.write(str(project_id))


@project_cli.command(name="list", help="List all projects currently registered.")
@click.pass_context
def project_list(ctx):
    resp = send_json_request("project_list", {})
    print("Projects:")
    for project in resp["projects"]:
        print(project)


@snapshot_cli.command(name="create", help="Create a snapshot of the current project.")
@click.option(
    "--description",
    help="A description of the snapshot",
    default=None)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation.")
def snapshot_create(description, yes):
    project_definition = load_project_or_throw()
    try:
        create_snapshot(project_definition, yes,
                description=description, local=True)
    except click.Abort as e:
        raise e
    except Exception as e:
        # Creating a snapshot can fail if the project is not found or if some
        # files cannot be copied (e.g., due to permissions).
        raise click.ClickException(e)

@snapshot_cli.command(name="delete", help="Delete a snapshot of the current project with the given UUID.")
@click.argument("uuid")
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation.")
def snapshot_delete(uuid, yes):
    project_definition = load_project_or_throw()
    try:
        delete_snapshot(project_definition.root, uuid, yes)
    except click.Abort as e:
        raise e
    except Exception as e:
        # Deleting a snapshot can fail if the project is not found.
        raise click.ClickException(e)


@snapshot_cli.command(name="list", help="List all snapshots of the current project.")
def snapshot_list():
    project_definition = load_project_or_throw()

    try:
        snapshots = list_snapshots(project_definition.root)
    except Exception as e:
        # Listing snapshots can fail if the project is not found.
        raise click.ClickException(e)

    if len(snapshots) == 0:
        print("No snapshots found.")
    else:
        print("Project snaphots:")
        for snapshot in snapshots:
            print(" {}".format(snapshot))

@snapshot_cli.command(name="describe", help="Describe metadata and files of a snapshot.")
@click.argument("name")
def snapshot_describe(name):
    try:
        snapshot = describe_snapshot(name)
    except Exception as e:
        # Describing a snapshot can fail if the snapshot does not exist.
        raise click.ClickException(e)
    print(snapshot)

@snapshot_cli.command(name="download", help="Download a snapshot.")
@click.argument("name")
@click.option("--target-directory", help="Directory this snapshot is downloaded to.")
def snapshot_download(name, target_directory):
    try:
        snapshot = describe_snapshot(name)
    except Exception as e:
        # The snapshot may not exist.
        raise click.ClickException(e)

    if not target_directory:
        target_directory = os.path.join(os.getcwd(), name)

    download_snapshot(snapshot["uuid"], target_directory=target_directory, apply_patch=True)

@session_cli.command(
    name="attach",
    help="Open a console for the given session.")
@click.option(
    "--name", help="Name of the session to open a console for.",
    default=None
)
@click.option("--tmux", help="Attach console to tmux.", is_flag=True)
@click.option("--screen", help="Attach console to screen.", is_flag=True)
def session_attach(name, tmux, screen):
    project_definition = load_project_or_throw()
    project_id = get_project_id(os.getcwd())
    resp = send_json_request("project_sessions", {
        "project_id": project_id,
        "session_name": name,
        })
    sessions = resp["sessions"]

    if len(sessions) != 1:
        raise click.ClickException("Multiple ({}) sessions found with name {}".format(len(sessions), name))

    session = sessions[0]
    ray.autoscaler.commands.attach_cluster(
        project_definition.cluster_yaml(),
        start=False,
        use_tmux=tmux,
        use_screen=screen,
        override_cluster_name=session["name"],
        new=False,
    )


@session_cli.command(
    name="commands",
    help="Print available commands for sessions of this project.")
def session_commands():
    project_definition = load_project_or_throw()
    print("Active project: " + project_definition.config["name"])
    print()

    commands = project_definition.config["commands"]

    for command in commands:
        print("Command \"{}\":".format(command["name"]))
        parser = argparse.ArgumentParser(command["name"], description=command.get("help"), add_help=False)
        params = command.get("params", [])
        for param in params:
            name = param.pop("name")
            if "type" in param: param.pop("type")
            parser.add_argument("--" + name, **param)
        help_string = parser.format_help()
        # Indent the help message by two spaces and print it.
        print("\n".join(["  " + line for line in help_string.split("\n")]))

@session_cli.command(
    name="start",
    context_settings=dict(ignore_unknown_options=True, ),
    help="Start a session based on the current project configuration.")
@click.argument("command", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--shell", help="If set, run the command as a raw shell command instead of looking up the command in the project.yaml.", is_flag=True)
@click.option(
    "--snapshot", help="If set, start the session from the given snapshot.", default=None)
@click.option(
    "--name", help="A name to tag the session with.", default=None)
def session_start(command, args, shell, snapshot, name):
    project_definition = load_project_or_throw()
    if not name:
        name = project_definition.config["name"]
    # Get the actual command to run. This also validates the command,
    # which should be done before the cluster is started.
    try:
        command, parsed_args, config = project_definition.get_command_info(
            command, args, shell, wildcards=True)
    except ValueError as e:
        raise click.ClickException(e)
    session_runs = ray_scripts.get_session_runs(name, command, parsed_args)

    if len(session_runs) > 1 and not config.get("tmux", False):
        logging.info("Using wildcards with tmux = False would not create "
                     "sessions in parallel, so we are overriding it with "
                     "tmux = True.")
        config["tmux"] = True

    project_id = get_project_id(os.getcwd())
    snapshot_uuid = get_or_create_snapshot(snapshot, project_definition, True, local=True)

    for run in session_runs:
        session_name = run["name"]
        resp = send_json_request("session_list", {
            "project_id": project_id,
            "session_name": session_name,
            })
        if len(resp["sessions"]) == 0:
            resp = send_json_request("session_create", {
                "project_id": project_id,
                "session_name": session_name,
                "snapshot_uuid": snapshot_uuid
                }, post=True)
            session_id = resp["id"]
        else:
            raise click.ClickException("Session with name {} already exists".format(session_name))

@session_cli.command(
    name="sync",
    help="Synchronize a session with a snapshot.")
@click.option(
    "--snapshot", help="The snapshot the session should be synchronized with.", default=None)
@click.option(
    "--name", help="The name of the session to synchronize.", default=None)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation. Confirmation is needed when no snapshot name is provided.")
def session_sync(snapshot, name, yes):
    project_definition = load_project_or_throw()
    project_id = get_project_id(os.getcwd())
    resp = send_json_request("project_sessions", {
        "project_id": project_id,
        "session_name": name,
        })
    sessions = resp["sessions"]

    if len(sessions) == 0:
        raise click.ClickException("No active session matching pattern {} found".format(name))

    # Sync the snapshot to all matching sessions.
    for session in sessions:
        send_json_request("session_sync", {"session_id": session["id"], "snapshot_id": snapshot}, post=True)


@session_cli.command(
    name="execute",
    context_settings=dict(ignore_unknown_options=True, ),
    help="Execute a command in a session.")
@click.argument("command", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--shell", help="If set, run the command as a raw shell command instead of looking up the command in the project.yaml.", is_flag=True)
@click.option(
    "--name", help="Name of the session to run this command on",
    default=None
)
def session_execute(command, args, shell, name):
    project_definition = load_project_or_throw()

    project_id = get_project_id(os.getcwd())
    resp = send_json_request("project_sessions", {
        "project_id": project_id,
        "session_name": name,
        })
    sessions = resp["sessions"]

    if len(sessions) == 0:
        raise click.ClickException("No active session matching pattern {} found".format(name))

    for session in sessions:
        resp = send_json_request("session_execute", {
            "session_id": session["id"],
            "command": command,
            "params": {},
            "shell": shell,
            }, post=True)

@session_cli.command(name="log", help="Show log for the current session.")
@click.option(
    "--name", help="Name of the session to run this command on",
    default=None
)
def session_log(name):
    project_id = get_project_id(os.getcwd())
    resp = send_json_request("project_sessions", {
        "project_id": project_id,
        "session_name": name,
        })
    sessions = resp["sessions"]
    if len(sessions) == 0:
        raise click.ClickException("No active session matching pattern {} found".format(name))
    for session in sessions:
        resp = send_json_request("session_execution_log", {
            "session_id": session["id"],
            "from_bytes": 0,
            })
        print(resp["log"])

@session_cli.command(name="stop", help="Stop the current session.")
@click.option(
    "--name", help="Name of the session to stop",
    default=None
)
@click.pass_context
def session_stop(ctx, name):
    project_id = get_project_id(os.getcwd())
    resp = send_json_request("project_sessions", {
        "project_id": project_id,
        "session_name": name,
        })
    sessions = resp["sessions"]
    if len(sessions) == 0:
        raise click.ClickException("No active session matching pattern {} found".format(name))

    for session in sessions:
        # Stop the session and mark it as stopped in the database.
        send_json_request("session_stop", {
            "session_id": session["id"],
            }, post=True)

@session_cli.command(name="list", help="List all sessions of the current project.")
@click.option(
    "--name",
    help="Name of the session. If provided, this prints the snapshots that were applied and commands that ran for all sessions that match this name.",
    default=None)
@click.option(
    "--all", help="List all sessions, including inactive ones.", is_flag=True)
def session_list(name, all):
    project_id = get_project_id(os.getcwd())
    project_definition = load_project_or_throw()
    print("Active project: " + project_definition.config["name"])

    resp = send_json_request("session_list", {
        "project_id": project_id,
        "session_name": name,
        "active_only": not all,
        })
    sessions = resp["sessions"]

    if name is None:
        print()
        table = []
        for session in sessions:
            created_at = humanize_timestamp(deserialize_datetime(session["created_at"]))
            record = [session["name"], created_at, session["latest_snapshot_uuid"]]
            if all:
                table.append([" Y" if session["active"] else " N"] + record)
            else:
                table.append(record)
        if not all:
            print(tabulate.tabulate(table, headers=["SESSION", "CREATED", "SNAPSHOT"], tablefmt="plain"))
        else:
            print(tabulate.tabulate(table, headers=["ACTIVE", "SESSION", "CREATED", "SNAPSHOT"], tablefmt="plain"))
    else:
        sessions = [session for session in sessions if session["name"] == name]
        for session in sessions:
            resp = send_json_request("session_describe", {
                "session_id": session["id"],
                })

            print()
            print("Snapshots applied to", session)
            for applied_snapshot in resp["applied_snapshots"]:
                created_at, snapshot = applied_snapshot
                created_at = humanize_timestamp(deserialize_datetime(created_at))
                print(" {}: {}".format(created_at, snapshot))
            print("Commands run during", session)
            for command in resp["commands"]:
                created_at, command = command
                created_at = humanize_timestamp(deserialize_datetime(created_at))
                print(" {}: '{}'".format(created_at, command))


cli.add_command(project_cli)
cli.add_command(session_cli)
cli.add_command(snapshot_cli)

def main():
    return cli()

if __name__ == '__main__':
    main()
