from genericpath import exists
from pathlib import Path
from rich import print
from rich.prompt import Prompt
from simple_term_menu import TerminalMenu

import boto3
import configparser
import os


def get_cluster_arn(profile: str):

    try:
        session = boto3.Session(profile_name=profile)
        # Call the boto3 client for ecs to list the cluster
        ecs_client = session.client('ecs')
        cluster_response = ecs_client.list_clusters(
            maxResults=10
        )
    except Exception as Err:
        print(f'ERROR: {Err}')
        exit(-1)   
        
    return cluster_response['clusterArns']


def get_service_arn(profile: str, cluster_name: str):
    
    try:
        session = boto3.Session(profile_name=profile)
        # Call the boto3 client for ecs to list the service from the cluster selected cluster
        ecs_client = session.client('ecs')
        service_response = ecs_client.list_services(
            cluster = cluster_name,
            maxResults=50,
            launchType='FARGATE',
        )
    except Exception as Err:
        print(f'ERROR: {Err}')
        exit(-1)        
    
    return service_response['serviceArns']


def get_task_arn(profile: str, cluster_name: str, service_name: str = ""):

    try:
        session = boto3.Session(profile_name=profile)
        # Call the boto3 client for ecs to list the task from the selected cluster & service
        ecs_client = session.client('ecs')
        task_response = ecs_client.list_tasks(
            cluster     = cluster_name,
            maxResults  = 100,
            serviceName = service_name,
        )
    except Exception as Err:
        print(f'ERROR: {Err}')
        exit(-1)        
    
    return task_response['taskArns']


def get_container_name(profile: str, cluster_name: str, task_name: str):
    
    # Instantiate a list to contain the container_name
    list_container_name = list()
    
    try:
        session = boto3.Session(profile_name=profile)
        ecs_client = session.client('ecs')
        container_response = ecs_client.describe_tasks(
            cluster=cluster_name,
            tasks=[
                task_name,
            ]
        )
    except Exception as Err:
        print(f'ERROR: {Err}')
        exit(-1)
    
    for task in container_response['tasks']:
        for container in task['containers']:
            list_container_name.append(container['name'])

    return list_container_name



def get_cluster_name(profile: str):
    
    # Instantiate a list to contain the cluster_name
    list_cluster_name = list()
    
    for cluster_arn in (get_cluster_arn(profile)):
        list_cluster_name.append(cluster_arn.partition('/')[2])
        
    return list_cluster_name


def get_service_name(profile: str, cluster_name: str):
    
    # Instantiate a list to contain the list_service_name
    list_service_name = list()
    
    for service_arn in (get_service_arn(profile, cluster_name)):
        list_service_name.append(service_arn.partition('/')[2])
        
    return list_service_name


def display_menu(menu_list: list, menu_title: str = ""):
    
    # Display the menu with terminal menu
    terminal_menu = TerminalMenu(menu_list, title=f'{menu_title}: \n')
    menu_entry_index = terminal_menu.show()
    
    return menu_entry_index


def check_credentials():
    print('Check AWS credentials ...')
    if exists((f'{Path.home()}/.aws/credentials')):
        print(f'Using the file {Path.home()}/.aws/credentials')
        config = configparser.ConfigParser()
        config.sections()
        config.read(f'{Path.home()}/.aws/credentials')

    else:
        print('###########################################################')
        print('####    WARNING !')
        print('####    AWS credentials file was not found under the ${HOME}/.aws/credentials path.')
        print('####    Please verify that you have got credentials file and you set aws region for your profile.')
        print('###########################################################\n')
        creds_path = Prompt.ask('Enter your aws credentials file path :sunglasses:')
        if exists(creds_path):
            config = configparser.ConfigParser()
            config.sections()
            config.read(creds_path)
            os.environ ['AWS_SHARED_CREDENTIALS_FILE'] = creds_path
        else:
            print(f'ERROR: The file {creds_path} doesn''t exist ! Bye bye')
            exit(-1)
    
    return config.sections()

def choose_credentials_profile():
    
    list_credentials_profiles = check_credentials()
    credentials_menu_entry_index = display_menu(list_credentials_profiles, menu_title='Choose the credentials to use')
    print(f'You choose to use AWS {list_credentials_profiles[credentials_menu_entry_index]} profile')
    return list_credentials_profiles[credentials_menu_entry_index]


def choose_cluster(profile: str):
    
    # Retrieve the cluster_arn list from the command list_cluster
    list_cluster_name = get_cluster_name(profile)
    cluster_menu_entry_index = display_menu(list_cluster_name, menu_title='Choose the cluster to list service from')
    
    return list_cluster_name[cluster_menu_entry_index]


def choose_service(profile: str, cluster_name: str):
    
    # Retrieve the cluster_arn list from the command list_cluster
    list_service_name = get_service_name(profile, cluster_name)
    service_menu_entry_index = display_menu(list_service_name, menu_title='Choose the service to list task from')
    
    return list_service_name[service_menu_entry_index]


def choose_task(profile: str, cluster_name: str, service_name: str):
    
    list_task_arn = get_task_arn(profile, cluster_name, service_name)
    task_menu_entry_index = display_menu(list_task_arn, menu_title='Choose the task to list container from')
    
    return list_task_arn[task_menu_entry_index]


def choose_container(profile: str, cluster_name: str, task_name: str):
    
    list_container_name = get_container_name(profile, cluster_name, task_name.partition('/')[2].partition('/')[2])
    container_menu_entry_index = display_menu(list_container_name, menu_title='Choose the container to connect')
    
    return list_container_name[container_menu_entry_index]