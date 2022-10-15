# aws_ecs_exec_command_cli

AWS ECS Exec command cli tool is aimed to connect to your docker instance running under ECS Fargate.

The `aws ecs execute-command` command is quite complicated to memory and the tool give you the ability to parse and retrieve:

- your clusters
- your services
- your tasks
- your container

To let you choose which one you want to connect into.

&nbsp;

## Installation

**Requirements**

You should have `aws-cli` already installed with credentials file.

&nbsp;

Create a virtualenv with python > 3.7

&nbsp;

```bash
source .venv3.7/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
❯ python main.py --help


Welcome in AWS ECS Exec command Cli !


 Usage: main.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                       │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                │
│ --help                        Show this message and exit.                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ get-ecs-connection                                                                                                                            │
│ list-cluster                                                                                                                                  │
│ list-service                                                                                                                                  │
│ list-task                                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

