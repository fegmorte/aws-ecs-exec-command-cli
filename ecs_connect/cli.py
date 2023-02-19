import sys
import subprocess
import typer

from ecs_connect import __app_name__, __version__
from ecs_connect.menu import make_choice
from ecs_connect.helpers import get_cluster_arn
from ecs_connect.helpers import get_service_arn
from ecs_connect.helpers import get_task_arn
from ecs_connect.helpers import get_task_defintion_arn
from ecs_connect.helpers import get_log_group

from rich import print
from typing import Optional


app = typer.Typer()


@app.command()
def list_cluster():
    """List cluster into an AWS account"""
    try:
        credentials_type = make_choice(choice="credentials_type")
        if credentials_type == "AWS_CREDENTIALS_FILE":
            profile_name = make_choice(choice="profile_name")
        else:
            profile_name = credentials_type

        print("Cluster(s) ARN available in your account: ")
        for cluster_arn in get_cluster_arn(profile_name):
            print(f"[green]{cluster_arn}[/green]")

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()


@app.command()
def list_service():
    """List service(s) into a cluster"""
    try:
        credentials_type = make_choice(choice="credentials_type")
        if credentials_type == "AWS_CREDENTIALS_FILE":
            profile_name = make_choice(choice="profile_name")
        else:
            profile_name = credentials_type

        cluster_name = make_choice(choice="cluster_name", profile=profile_name)

        print(f"Service(s) ARN in cluster {cluster_name}: ")
        for service_arn in get_service_arn(profile_name, cluster_name):
            print(f"[green]{service_arn}[/green]")

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()


@app.command()
def list_task():
    """List task(s) into a service into a cluster"""
    try:
        credentials_type = make_choice(choice="credentials_type")
        if credentials_type == "AWS_CREDENTIALS_FILE":
            profile_name = make_choice(choice="profile_name")
        else:
            profile_name = credentials_type

        cluster_name = make_choice(choice="cluster_name", profile=profile_name)

        service_name = make_choice(
            choice="service_name", profile=profile_name, cluster_name=cluster_name
        )

        print(f"Task(s) ARN in cluster {cluster_name} and service {service_name}: ")
        for task_arn in get_task_arn(
            profile=profile_name, cluster_name=cluster_name, service_name=service_name
        ):
            print(f"[green]{task_arn}[/green]")

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()


@app.command("connect")
def ecs_connect():
    """Connect to an ECS Fargate container"""
    try:
        credentials_type = make_choice(choice="credentials_type")
        if credentials_type == "AWS_CREDENTIALS_FILE":
            profile_name = make_choice(choice="profile_name")
        else:
            profile_name = credentials_type

        cluster_name = make_choice(choice="cluster_name", profile=profile_name)

        service_name = make_choice(
            choice="service_name", profile=profile_name, cluster_name=cluster_name
        )

        task_name = make_choice(
            choice="task_arn",
            profile=profile_name,
            cluster_name=cluster_name,
            service_name=service_name,
        )

        container_name = make_choice(
            choice="container_name",
            profile=profile_name,
            cluster_name=cluster_name,
            task_name=task_name,
        )

        print(f"Connection to {container_name} ...")
        command = f'aws ecs execute-command --region eu-west-1 --cluster {cluster_name} --task {task_name} --container {container_name} --command "/bin/bash" --interactive --profile {profile_name}'
        subprocess.run(command, shell=True)

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()


@app.command("tail")
def tail_logs():
    """Tail logs of a selected  ECS container"""
    try:
        credentials_type = make_choice(choice="credentials_type")
        if credentials_type == "AWS_CREDENTIALS_FILE":
            profile_name = make_choice(choice="profile_name")
        else:
            profile_name = credentials_type

        cluster_name = make_choice(choice="cluster_name", profile=profile_name)

        service_name = make_choice(
            choice="service_name", profile=profile_name, cluster_name=cluster_name
        )

        task_name = make_choice(
            choice="task_arn",
            profile=profile_name,
            cluster_name=cluster_name,
            service_name=service_name,
        )

        container_name = make_choice(
            choice="container_name",
            profile=profile_name,
            cluster_name=cluster_name,
            task_name=task_name,
        )

        task_defition_arn = get_task_defintion_arn(
            profile=profile_name, cluster_name=cluster_name, task_name=task_name
        )

        log_group = get_log_group(
            profile=profile_name,
            container_name=container_name,
            task_definition_arn=task_defition_arn,
        )

        print(f"Retrieving log for {container_name} ...")
        command = (
            f"aws logs tail {log_group} --follow --color=on --profile {profile_name}"
        )

        subprocess.run(command, shell=True)

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()


@app.command("exec-command")
def exec_command(
    command: str = typer.Option(..., help=" Command to execute"),
    output_filename: Optional[str] = typer.Option(
        "", help="Filename to output results"
    ),
):
    """Execute manage.py command with args"""
    try:
        credentials_type = make_choice(choice="credentials_type")
        if credentials_type == "AWS_CREDENTIALS_FILE":
            profile_name = make_choice(choice="profile_name")
        else:
            profile_name = credentials_type

        cluster_name = make_choice(choice="cluster_name", profile=profile_name)

        service_name = make_choice(
            choice="service_name", profile=profile_name, cluster_name=cluster_name
        )

        task_name = make_choice(
            choice="task_arn",
            profile=profile_name,
            cluster_name=cluster_name,
            service_name=service_name,
        )

        container_name = make_choice(
            choice="container_name",
            profile=profile_name,
            cluster_name=cluster_name,
            task_name=task_name,
        )

        print(f"Execute {command}")

        command = f'aws ecs execute-command --region eu-west-1 --cluster {cluster_name} --task {task_name} --container {container_name} --command "{command}" --interactive --profile {profile_name}'
        if output_filename:
            command += f"> {output_filename}"
        subprocess.run(command, shell=True)

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
