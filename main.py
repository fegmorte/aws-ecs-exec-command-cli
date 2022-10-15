from helpers import choose_credentials_profile
from helpers import choose_cluster
from helpers import choose_service
from helpers import choose_task
from helpers import choose_container
from helpers import get_cluster_arn
from helpers import get_service_arn
from helpers import get_task_arn

from rich import print

import subprocess
import typer

app = typer.Typer()

@app.command()
def list_cluster():

    # Check and choose credentials
    profile_name = choose_credentials_profile()
    
    print('Cluster(s) ARN available in your account: ')
    for cluster_arn in (get_cluster_arn(profile_name)):
        print(cluster_arn)


@app.command()
def list_service():

    # Check and choose credentials
    profile_name = choose_credentials_profile()
    
    # Retrieve the cluster_arn list from the command list_cluster
    cluster_name = choose_cluster(profile_name)    

    print(f'Service(s) ARN in cluster {cluster_name}: ')
    for service_arn in get_service_arn(profile_name, cluster_name):
        print(service_arn)


@app.command()
def list_task():
    
    # Check and choose credentials
    profile_name = choose_credentials_profile()
        
    # Retrieve the cluster_name list from the command list_cluster
    cluster_name = choose_cluster(profile_name)
    
    # Retrieve the service_name list from the command list_cluster
    service_name = choose_service(profile_name, cluster_name)
    
    print(f'Task(s) ARN in cluster {cluster_name} and service {service_name}: ')
    for task_arn in get_task_arn(profile_name, cluster_name, service_name):
        print(task_arn)
        
    
@app.command()
def get_ecs_connection():
    
    # Check and choose credentials
    profile_name = choose_credentials_profile()
    
    # Retrieve the cluster_arn list
    cluster_name = choose_cluster(profile_name)  
    
    # Retrieve the service_name list
    service_name = choose_service(profile_name, cluster_name)
    
    # Retrieve the task_name list
    task_name = choose_task(profile_name, cluster_name, service_name)
    
    # Retrieve the container_name    
    container_name = choose_container(profile_name, cluster_name, task_name)
    
    command = f'aws ecs execute-command --region eu-west-1 --cluster {cluster_name} --task {task_name} --container {container_name} --command "/bin/sh" --interactive --profile {profile_name}'
    subprocess.run(command, shell=True)
 
    
if __name__ == "__main__":
    print("\n")
    print('Welcome in AWS ECS Exec command Cli !\n')
    app()
