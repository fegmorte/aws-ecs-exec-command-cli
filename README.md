# ecs_connect_cli

AWS ECS Exec command cli tool is aimed to :

- connect to your container instance running under ECS Fargate.
- tail the log from cloudwatch logs (if you configure a logconfiguration in your task definition)
- update secret value into secret manager

&nbsp;

The `aws ecs execute-command` command is quite complicated to remember and the tool give you the ability to parse and retrieve:

- your clusters
- your services
- your tasks
- your container

To let you choose which one you want to connect into.

**Enhancements** :sunglasses:
You can now connect to ECS and tail your logs from an EC2 instance or AWS CloudShell without the need of aws cli and aws credentials file.

At start, you are asked what kind of credentials you want to use and which default region.

You can now also update your secret directly from the command line.

```bash
ecs-connect-cli update-secret your-secret-name
```

I also add the possibility to run directly with pipx 
```bash
pipx run ecs-connect-cli --help
```


&nbsp;

## Installation

**Requirements**


- Install awscli via [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html] (not necessary if you are connected to an EC2 instance)

- Install ssm  tools via [https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html]


&nbsp;

To install you have several options:

- Install it globally with your pip:
```bash
pip install ecs-connect-cli
```

- Install it into a virtualenv (after creating a virtualenv with the tool of your choice):
```bash
source .venv_3.11.0/bin/activate
pip install ecs-connect-cli
```

- Run the cli directly with [pipx](https://pipx.pypa.io/latest/)
```bash
pipx run ecs-connect-cli --help
```


&nbsp;

if it is the first time you connect to aws-cli, you have to get credentials key from your aws administrator.

&nbsp;

## Usage

If you use it with with pip, you can call the CLI as below or directly call it with pipx

```bash
ecs-connect-cli --help


Welcome in AWS ECS Exec command Cli !

                                                                                                                                                                                       
 Usage: ecs_connect_cli [OPTIONS] COMMAND [ARGS]...                                                                                                                                        
                                                                                                                                                                                       
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
| update-secret                     Update secret from secret manager                                                                        |
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

&nbsp;

## Testing

The project now contains two test layers:

- unit tests (fast, mocked CLI/AWS boundaries)
- integration tests (real boto3 calls against MiniStack)

### Local setup

Use a Python version supported by this project (3.9 to 3.14).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run unit tests

```bash
pytest -m "not integration" -q
```

### Run integration tests with MiniStack

Start MiniStack:

```bash
docker run --rm -p 4566:4566 ministackorg/ministack
```

Run integration tests in another terminal:

```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export ECS_CONNECT_AWS_ENDPOINT_URL=http://localhost:4566
pytest -m "integration" -q
```

You can also use `AWS_ENDPOINT_URL` instead of `ECS_CONNECT_AWS_ENDPOINT_URL`.

### Run all tests

```bash
pytest -q
```

&nbsp;

Thanks to Typer from [@tiangolo](https://typer.tiangolo.com/)

Thanks to [@kraymer](https://github.com/kraymer) for echoprompt :sunglasses:
