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

** NEW ** 
You can now connect to ECS and tail your logs from an EC2 instance without the need of aws cli and aws credentials file.

At start, you are asked  what kind of credentials you want to use and which default region.

&nbsp;

## Installation

**Requirements**

- Install awscli via [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html]

- Install ssm  tools via [https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html]


&nbsp;

You should install the requirements via the pip install below.

&nbsp;

Create a virtualenv with python > 3.7

&nbsp;

```bash
source .venv3.7/bin/activate
pip install -r requirements.txt
```

&nbsp;

if it is the first time you connect to awc-cli, you have to get credentials key from your aws administrator.

&nbsp;

## Usage

```bash
❯ python -m ecs_connect --help


Welcome in AWS ECS Exec command Cli !

                                                                                                                                                                                       
 Usage: ecs_connect [OPTIONS] COMMAND [ARGS]...                                                                                                                                        
                                                                                                                                                                                       
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show the application's version and exit.                                                                   │
│ --install-completion            Install completion for the current shell.                                                                  │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                           │
│ --help                          Show this message and exit.                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ connect                           Connect to an ECS Fargate container                                                                      │
│ exec-command                      Execute manage.py command with args                                                                      │
│ list-cluster                      List cluster into an AWS account                                                                         │
│ list-service                      List service(s) into a cluster                                                                           │
│ list-task                         List task(s) into a service into a cluster                                                               │
│ tail                              Tail logs of a selected  ECS container                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

&nbsp;

Thanks to Typer from [@tiangolo](https://typer.tiangolo.com/)

Thanks to simple-term-menu [@IngoMeyer441](https://github.com/IngoMeyer441/simple-term-menu)