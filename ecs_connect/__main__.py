# ecs_connect/__main__.py

from ecs_connect import cli, __app_name__

def main():
    print("\n")
    print('Welcome in AWS ECS Exec command Cli !\n')
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()