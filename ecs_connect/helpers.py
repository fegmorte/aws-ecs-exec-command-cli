import tempfile
import os
import json
import hashlib
from subprocess import call
from ecs_connect.session import get_session
from rich import print


def get_cluster_arn(profile: str) -> list:
    """Retrieve cluster arn

    Args:
        profile (str): aws profile

    Returns:
        list: List of cluster(s) arn
    """
    cluster_response = get_session(profile=profile, resource="ecs", action="list_clusters")

    return cluster_response["clusterArns"]


def get_service_arn(profile: str, cluster_name: str) -> list:
    """Retrieve service arn from a cluster

    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service

    Returns:
        list: List of service(s) arn
    """
    service_response = get_session(
        profile=profile, resource="ecs", cluster_name=cluster_name, action="list_services"
    )

    return service_response["serviceArns"]


def get_task_arn(profile: str, cluster_name: str, service_name: str) -> list:
    """Retrieve task(s) arn from a service into a cluster

    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service
        service_name (str): name of the service to retrieve task

    Returns:
        list: List of task(s) arn
    """
    task_response = get_session(
        profile=profile,
        resource="ecs", 
        cluster_name=cluster_name,
        service_name=service_name,
        action="list_tasks",
    )

    return task_response["taskArns"]


def get_container_name(profile: str, cluster_name: str, task_name: str) -> list:
    """Retrieve container name from task into a cluster

    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service
        task_name (str): name of the task to retrieve the container name

    Returns:
        list: List of container name
    """
    list_container_name = list()

    container_response = get_session(
        profile=profile,
        resource="ecs", 
        cluster_name=cluster_name,
        task_name=task_name,
        action="describe_tasks",
    )

    for task in container_response["tasks"]:
        for container in task["containers"]:
            list_container_name.append(container["name"])

    return list_container_name


def get_task_defintion_arn(profile: str, cluster_name: str, task_name: str) -> str:
    """Retrieve task definition arn from a container

    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service
        task_name (str): name of the task to retrieve the task defintion arn

    Returns:
        str: Task definition arn
    """
    container_response = get_session(
        profile=profile,
        resource="ecs", 
        cluster_name=cluster_name,
        task_name=task_name,
        action="describe_tasks",
    )
    return container_response["tasks"][0]["taskDefinitionArn"]


def get_log_group(profile: str, container_name: str, task_definition_arn: str) -> str:
    """Retrieve the log group of task definition to get cloudwatch logs

    Args:
        profile (str): aws profile
        container_name (str): name of the container to target in task definition
        task_definition_arn (str): task definition arn to retrieve log group

    Returns:
        str: Log group name
    """
    log_group_response = get_session(
        profile=profile,
        resource="ecs", 
        task_definition_arn=task_definition_arn,
        action="describe_task_definition",
    )

    for container in log_group_response["taskDefinition"]["containerDefinitions"]:
        if container["name"] == container_name:
            if "logConfiguration" in container:
                return container["logConfiguration"]["options"]["awslogs-group"]
            else:
                print(
                    f"[red]ERROR: LogConfiguration not found for {container_name} ![/red]"
                )
                print("Bye Bye !")
                exit(-1)


def get_cluster_name(profile: str) -> list:
    """Retrieve list of cluster name from aws profile

    Args:
        profile (str): aws profile

    Returns:
        list: List of cluster name instead of arn
    """
    list_cluster_name = list()

    for cluster_arn in get_cluster_arn(profile):
        list_cluster_name.append(cluster_arn.partition("/")[2])

    return list_cluster_name


def get_service_name(profile: str, cluster_name: str) -> list:
    """Retrieve list of service into a cluster

    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service

    Returns:
        list: List of service name
    """
    list_service_name = list()

    for service_arn in get_service_arn(profile, cluster_name):
        list_service_name.append(service_arn.partition("/")[2])

    return list_service_name


def get_secret_value(profile: str, secret_name: str) -> str:
    """Retrieve secret value for editing

    Args:
        profile (str): aws profile
        secret_name (str): secret name 
        
    Returns:
        str: Value of the secret
    """    
    client = get_session(
        profile=profile,
        resource="secretsmanager",
        )    
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        print(f"ERROR: The secret: {secret_name} doesn't exist within your profile: {profile}")
        print("HINT: Double check your credentials according the secret you want to update.")
        exit(-1)   
    
    return response["SecretString"]


def edit_secret_value(secret_value: dict) -> str:
    """Edit the secret value

    Args:
        secret_value (str): secret string to update
        
    Returns:
        str: Value of the secret
    """    
    try:
        # Get the text editor from the shell, otherwise default to Vim
        EDITOR = os.environ.get('EDITOR','vim')
        
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".tmp", delete=True) as tf:

            json.dump(secret_value, tf, sort_keys=True, indent=4)
            # Flush the I/O buffer to make sure the data is written to the file
            tf.flush()

            original_file_md5 = md5(tf.name)
            # Open the file with the text editor
            call([EDITOR, tf.name])

            # Reopen the file to read the edited data
            with open(tf.name, 'r') as tf:

                # Read the file data into a variable
                edited_message = tf.read()
                
                # Return the data
                final_file_md5 = md5(tf.name)
                
                return original_file_md5, final_file_md5, edited_message
            
    except Exception as Err:
        print(f"ERROR: {Err}")
        exit(-1)        
        
def update_secret_string(profile: str, secret_name: str, secret_string: str) -> str:     
    """Update secret string for the secret name

    Args:
        profile (str): aws profile
        secret_name (str): secret name 
        secret_string (str): secret string to update
        
    Returns:
        str: Value of the secret
    """    
    client = get_session(
        profile=profile,
        resource="secretsmanager",
        )     
    
    response = client.update_secret(
                SecretId=secret_name,
                SecretString=secret_string
            )
    return response


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()