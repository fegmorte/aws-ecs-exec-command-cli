from ecs_connect.credentials import check_credentials
from ecs_connect.credentials import which_credentials
from ecs_connect.credentials import which_region
from ecs_connect.helpers import get_cluster_name
from ecs_connect.helpers import get_container_name
from ecs_connect.helpers import get_service_name
from ecs_connect.helpers import get_task_arn

from simple_term_menu import TerminalMenu


def display_menu(menu_list: list, menu_title: str = "") -> int:
    """Display menu and retrieve the index of thechoice

    Args:
        menu_list (list): list of choice to display
        menu_title (str, optional): title to display for selection. Defaults to "".

    Returns:
        int: Index of the choice in the menu
    """
    terminal_menu = TerminalMenu(menu_list, title=f"{menu_title}: \n")
    menu_entry_index = terminal_menu.show()

    return menu_entry_index


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

    # choose_container
    if choice == "container_name":
        list_results = get_container_name(
            profile, cluster_name, task_name.partition("/")[2].partition("/")[2]
        )
        menu_title = "Choose the container to connect"

    # choose_task
    elif choice == "task_arn":
        list_results = get_task_arn(profile, cluster_name, service_name)
        menu_title = "Choose the task to list container from"

    # choose_service
    elif choice == "service_name":
        list_results = get_service_name(profile, cluster_name)
        menu_title = "Choose the service to list task from"

    # choose_cluster
    elif choice == "cluster_name":
        list_results = get_cluster_name(profile)
        menu_title = "Choose the cluster to list service from"

    # choose_credentials_profile
    elif choice == "profile_name":
        list_results = check_credentials()
        menu_title = "Choose the credentials to use"

    # choose which type of credentials to use
    elif choice == "credentials_type":
        list_results = which_credentials()
        menu_title = "Which type of credentials would you use"

    # choose which region to use
    elif choice == "region_name":
        list_results = which_region()
        menu_title = "Choose the default AWS region to use"

    # Display the menu
    index_menu = display_menu(list_results, menu_title=menu_title)

    return list_results[index_menu]
