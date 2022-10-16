import configparser
import os

from genericpath import exists
from pathlib import Path
from rich.prompt import Prompt
from rich import print


def check_credentials() -> list:
    """Check and retrieve AWS credentials

    Returns:
        list: List of AWS profiles retrieve from credentials file
    """
    print('[green]Check AWS credentials ...[/green]')
    if exists((f'{Path.home()}/.aws/credentials')):
        print(f'Using the file {Path.home()}/.aws/credentials')
        config = configparser.ConfigParser()
        config.sections()
        config.read(f'{Path.home()}/.aws/credentials')

    else:
        print('[bold red]WARNING ![/bold red]')
        print('[bold red]AWS credentials file was not found under the ${HOME}/.aws/credentials path.[/bold red] \n')
        print('[bold red]Please verify that you have got credentials file and you set aws region for your profile.[/bold red] \n')
        creds_path = Prompt.ask('[green]Enter your aws credentials file path [/green]')
        if exists(creds_path):
            config = configparser.ConfigParser()
            config.sections()
            config.read(creds_path)
            os.environ ['AWS_SHARED_CREDENTIALS_FILE'] = creds_path
        else:
            print(f'ERROR: The file {creds_path} doesn''t exist ! Bye bye')
            exit(-1)
    
    return config.sections()