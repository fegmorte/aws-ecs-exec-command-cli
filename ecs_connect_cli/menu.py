from ecs_connect_cli.credentials import check_credentials
from ecs_connect_cli.credentials import which_credentials
from ecs_connect_cli.credentials import which_region
from ecs_connect_cli.helpers import get_cluster_name
from ecs_connect_cli.helpers import get_container_name
from ecs_connect_cli.helpers import get_service_name
from ecs_connect_cli.helpers import get_task_arn


def make_choice(
    choice: str = None,
    profile: str = None,
    cluster_name: str = None,
    service_name: str = None,
    task_name: str = None,
) -> str:
    """Generic function to make choice in a list displayed

    Args:
        profile (str, optional): aws profile. Defaults to None.
        cluster_name (str, optional): name of the cluster to retrieve service. Defaults to None.
        service_name (str, optional): name of the service to retrieve task. Defaults to None.
        task_name (str, optional): name of the task to retrieve the container name. Defaults to None.

    Returns:
        str: String of the choice in the menu
    """

    list_results = ""

    # choose_container
    if choice == "container_name":
        list_results = get_container_name(
            profile, cluster_name, task_name.partition("/")[2].partition("/")[2]
        )

    # choose_task
    elif choice == "task_arn":
        list_results = get_task_arn(profile, cluster_name, service_name)

    # choose_service
    elif choice == "service_name":
        list_results = get_service_name(profile, cluster_name)

    # choose_cluster
    elif choice == "cluster_name":
        list_results = get_cluster_name(profile)

    # choose_credentials_profile
    elif choice == "profile_name":
        list_results = check_credentials()

    # choose which type of credentials to use
    elif choice == "credentials_type":
        list_results = which_credentials()

    # choose which region to use
    elif choice == "region_name":
        list_results = which_region()

    return list_results
