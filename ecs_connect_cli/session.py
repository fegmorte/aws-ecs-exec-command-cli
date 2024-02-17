import boto3


def get_session(
    profile: str = None,
    resource: str = None,
    cluster_name: str = None,
    service_name: str = None,
    task_name: str = None,
    task_definition_arn: str = None,
    action: str = None,
) -> list:
    """Generic function to call boto3 function to retrieve data from AWS

    Args:
        profile (str, optional): aws profile. Defaults to None.
        cluster_name (str, optional): name of the cluster to retrieve service. Defaults to None.
        service_name (str, optional): name of the service to retrieve task. Defaults to None.
        task_name (str, optional): name of the task to retrieve the container name. Defaults to None.
        task_definition_arn (str, optional): task definition arn to retrieve log group. Defaults to None.
        action (str, optional): boto3 action to call. Defaults to None.

    Returns:
        list: JSON response from boto3 call
    """
    try:
        if profile == "EC2_INSTANCE_METADATA":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=profile)
        
        client = session.client(resource)
        
        if resource == "ecs":
            if action == "list_clusters":
                response = client.list_clusters(maxResults=20)

            if action == "list_services":
                response = client.list_services(
                    cluster=cluster_name,
                    maxResults=50,
                    launchType="FARGATE",
                )

            if action == "list_tasks":
                response = client.list_tasks(
                    cluster=cluster_name,
                    maxResults=100,
                    serviceName=service_name,
                )

            if action == "describe_tasks":
                response = client.describe_tasks(
                    cluster=cluster_name,
                    tasks=[
                        task_name,
                    ],
                )

            if action == "describe_task_definition":
                response = client.describe_task_definition(
                    taskDefinition=task_definition_arn,
                )

        if resource == "secretsmanager":
            return client
        
    except Exception as Err:
        print(f"ERROR: {Err}")
        exit(-1)

    return response
