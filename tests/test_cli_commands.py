import os
import re

from typer.testing import CliRunner

from ecs_connect_cli import cli

runner = CliRunner()
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def _fake_make_choice(choice, profile=None, cluster_name=None, service_name=None, task_name=None):
    choices = {
        "profile_name": ["dev-profile"],
        "region": ["us-east-1"],
        "cluster_name": ["cluster-a"],
        "service_name": ["service-a"],
        "task_arn": ["arn:aws:ecs:us-east-1:111111111111:task/cluster-a/task-1"],
        "container_name": ["container-a"],
    }
    return choices[choice]


def test_root_help():
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    assert "Show the application's version and exit." in result.stdout
    assert "exec-command" in result.stdout


def test_exec_command_requires_command_option():
    result = runner.invoke(cli.app, ["exec-command"])
    raw_output = f"{result.stdout}\n{result.stderr}"
    output = ANSI_ESCAPE_RE.sub("", raw_output)
    assert result.exit_code != 0
    assert "Missing option" in output
    assert "--command" in output


def test_connect_builds_expected_command_with_profile(monkeypatch):
    prompts = iter(
        [
            "AWS_CREDENTIALS_FILE",
            "dev-profile",
            "cluster-a",
            "service-a",
            "arn:aws:ecs:us-east-1:111111111111:task/cluster-a/task-1",
            "container-a",
        ]
    )
    command_run = {}

    monkeypatch.setattr(cli, "make_choice", _fake_make_choice)
    monkeypatch.setattr(cli.prompt, "prompt_choice", lambda *_args, **_kwargs: next(prompts))
    monkeypatch.setattr(
        cli.subprocess, "run", lambda command, shell: command_run.update({"command": command, "shell": shell})
    )

    result = runner.invoke(cli.app, ["connect"])
    assert result.exit_code == 0
    assert command_run["shell"] is True
    assert '--command "/bin/bash" --interactive' in command_run["command"]
    assert "--profile dev-profile" in command_run["command"]


def test_tail_uses_region_from_ec2_metadata(monkeypatch):
    prompts = iter(
        [
            "EC2_INSTANCE_METADATA",
            "us-east-1",
            "cluster-a",
            "service-a",
            "arn:aws:ecs:us-east-1:111111111111:task/cluster-a/task-1",
            "container-a",
        ]
    )
    command_run = {}
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.setattr(cli, "make_choice", _fake_make_choice)
    monkeypatch.setattr(cli.prompt, "prompt_choice", lambda *_args, **_kwargs: next(prompts))
    monkeypatch.setattr(cli, "get_task_defintion_arn", lambda **_kwargs: "task-definition-1")
    monkeypatch.setattr(cli, "get_log_group", lambda **_kwargs: "/aws/ecs/cluster-a")
    monkeypatch.setattr(
        cli.subprocess, "run", lambda command, shell: command_run.update({"command": command, "shell": shell})
    )

    result = runner.invoke(cli.app, ["tail"])
    assert result.exit_code == 0
    assert os.environ["AWS_DEFAULT_REGION"] == "us-east-1"
    assert command_run["command"] == "aws logs tail /aws/ecs/cluster-a --follow --color=on"


def test_exec_command_builds_expected_command_with_output(monkeypatch):
    prompts = iter(
        [
            "AWS_CREDENTIALS_FILE",
            "dev-profile",
            "cluster-a",
            "service-a",
            "arn:aws:ecs:us-east-1:111111111111:task/cluster-a/task-1",
            "container-a",
        ]
    )
    command_run = {}

    monkeypatch.setattr(cli, "make_choice", _fake_make_choice)
    monkeypatch.setattr(cli.prompt, "prompt_choice", lambda *_args, **_kwargs: next(prompts))
    monkeypatch.setattr(
        cli.subprocess, "run", lambda command, shell: command_run.update({"command": command, "shell": shell})
    )

    result = runner.invoke(
        cli.app,
        ["exec-command", "--command", "printenv", "--output-filename", "out.txt"],
    )
    assert result.exit_code == 0
    assert '--command "printenv" --interactive' in command_run["command"]
    assert "--profile dev-profile" in command_run["command"]
    assert command_run["command"].endswith("> out.txt")
