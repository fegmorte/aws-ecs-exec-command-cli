# aws-ecs-exec-command-cli

AWS ECS Exec command cli tool is aimed to :

- connect to your container instance running under ECS Fargate.
- tail the log from cloudwatch logs (if you configure a logconfiguration in your task definition)

&nbsp;

The `aws ecs execute-command` command is quite complicated to remember and the tool give you the ability to parse and retrieve:

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
❯ python -m ecs_connect --help            


Welcome in AWS ECS Exec command Cli !

                                                                                                                                                                          
 Usage: ecs_connect [OPTIONS] COMMAND [ARGS]...                                                                                                                           
                                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show the application version and exit.                                                                                               │
│ --install-completion            Install completion for the current shell.                                                                                              │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                       │
│ --help                          Show this message and exit.                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ get-ecs-connection                                  Connect to an ECS Fargate container                                                                                │
│ get-logs                                            Tail logs of a selected  ECS container                                                                             │
│ list-cluster                                        List cluster into an AWS account                                                                                   │
│ list-service                                        List service(s) into a cluster                                                                                     │
│ list-task                                           List task(s) into a service into a cluster                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```

&nbsp;

Thanks to Typer from [@tiangolo](https://typer.tiangolo.com/)

Thanks to simple-term-menu [@IngoMeyer441](https://github.com/IngoMeyer441/simple-term-menu)