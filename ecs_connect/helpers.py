# ecs_connect/helpers.py

from ecs_connect.session import get_ecs_data


def get_cluster_arn(profile: str) -> list:
    """Retrieve cluster arn
    
    Args:
        profile (str): aws profile

    Returns:
        list: List of cluster(s) arn
    """
    cluster_response = get_ecs_data(profile=profile, action='list_clusters')
    
    return cluster_response['clusterArns']


def get_service_arn(profile: str, cluster_name: str)->list:
    """Retrieve service arn from a cluster
    
    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service

    Returns:
        list: List of service(s) arn
    """
    service_response = get_ecs_data(profile=profile, 
                                    cluster_name=cluster_name, 
                                    action='list_services')
    
    return service_response['serviceArns']


def get_task_arn(profile: str, cluster_name: str, service_name: str) -> list:
    """Retrieve task(s) arn from a service into a cluster
    
    Args:
        profile (str): aws profile
        cluster_name (str): name of the cluster to retrieve service
        service_name (str): name of the service to retrieve task

    Returns:
        list: List of task(s) arn
    """
    task_response = get_ecs_data(profile=profile, 
                                    cluster_name=cluster_name,
                                    service_name=service_name,
                                    action='list_tasks')
    
    return task_response['taskArns']


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
    
    container_response = get_ecs_data(profile=profile, 
                                    cluster_name=cluster_name,
                                    task_name=task_name,
                                    action='describe_tasks')
    
    for task in container_response['tasks']:
        for container in task['containers']:
            list_container_name.append(container['name'])

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
    container_response = get_ecs_data(profile=profile, 
                                    cluster_name=cluster_name,
                                    task_name=task_name,
                                    action='describe_tasks')
    return (container_response['tasks'][0]['taskDefinitionArn'])


def get_log_group(profile: str, container_name: str, task_definition_arn: str) -> str:
    """Retrieve the log group of task definition to get cloudwatch logs
    
    Args:
        profile (str): aws profile
        container_name (str): name of the container to target in task definition
        task_definition_arn (str): task definition arn to retrieve log group

    Returns:
        str: Log group name
    """
    log_group_response = get_ecs_data(profile=profile, 
                                    task_definition_arn=task_definition_arn,
                                    action='describe_task_definition')
    
    for container in log_group_response['taskDefinition']['containerDefinitions']:
        if container['name'] == container_name:
            return (container['logConfiguration']['options']['awslogs-group'])


def get_cluster_name(profile: str) -> list:
    """Retrieve list of cluster name from aws profile
    
    Args:
        profile (str): aws profile

    Returns:
        list: List of cluster name instead of arn
    """
    list_cluster_name = list()
    
    for cluster_arn in (get_cluster_arn(profile)):
        list_cluster_name.append(cluster_arn.partition('/')[2])
        
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
    
    for service_arn in (get_service_arn(profile, cluster_name)):
        list_service_name.append(service_arn.partition('/')[2])
        
    return list_service_name








