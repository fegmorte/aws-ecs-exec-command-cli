import os
import uuid

import boto3
import pytest

from ecs_connect_cli.helpers import (
    get_cluster_arn,
    get_log_group,
    get_secret_value,
    get_service_arn,
    get_task_arn,
    update_secret_string,
)


@pytest.fixture(scope="module")
def aws_env():
    original_env = {
        "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "AWS_DEFAULT_REGION": os.environ.get("AWS_DEFAULT_REGION"),
        "ECS_CONNECT_AWS_ENDPOINT_URL": os.environ.get("ECS_CONNECT_AWS_ENDPOINT_URL"),
    }
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["ECS_CONNECT_AWS_ENDPOINT_URL"] = "http://localhost:4566"
    yield
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture(scope="module")
def ecs_client(aws_env):
    return boto3.client(
        "ecs",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


@pytest.fixture(scope="module")
def secrets_client(aws_env):
    return boto3.client(
        "secretsmanager",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


@pytest.fixture(scope="module")
def ecs_seed(ecs_client):
    suffix = uuid.uuid4().hex[:8]
    cluster_name = f"it-cluster-{suffix}"
    service_name = f"it-service-{suffix}"
    family = f"it-family-{suffix}"
    log_group = f"/ecs/{cluster_name}"

    cluster = ecs_client.create_cluster(clusterName=cluster_name)
    task_definition = ecs_client.register_task_definition(
        family=family,
        networkMode="bridge",
        requiresCompatibilities=["EC2"],
        cpu="256",
        memory="512",
        containerDefinitions=[
            {
                "name": "app",
                "image": "public.ecr.aws/docker/library/alpine:latest",
                "essential": True,
                "memory": 128,
                "cpu": 1,
                "command": ["sleep", "10"],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": log_group,
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs",
                    },
                },
            }
        ],
    )

    ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_definition["taskDefinition"]["taskDefinitionArn"],
        desiredCount=0,
        launchType="EC2",
    )

    return {
        "cluster_name": cluster_name,
        "cluster_arn": cluster["cluster"]["clusterArn"],
        "service_name": service_name,
        "task_definition_arn": task_definition["taskDefinition"]["taskDefinitionArn"],
        "log_group": log_group,
    }


@pytest.mark.integration
def test_helpers_list_cluster_service_and_tasks(ecs_seed):
    profile = "EC2_INSTANCE_METADATA"
    cluster_arns = get_cluster_arn(profile=profile)
    service_arns = get_service_arn(profile=profile, cluster_name=ecs_seed["cluster_name"])
    task_arns = get_task_arn(
        profile=profile,
        cluster_name=ecs_seed["cluster_name"],
        service_name=ecs_seed["service_name"],
    )

    assert ecs_seed["cluster_arn"] in cluster_arns
    assert any(ecs_seed["service_name"] in service_arn for service_arn in service_arns)
    assert isinstance(task_arns, list)


@pytest.mark.integration
def test_helper_get_log_group_from_task_definition(ecs_seed):
    log_group = get_log_group(
        profile="EC2_INSTANCE_METADATA",
        container_name="app",
        task_definition_arn=ecs_seed["task_definition_arn"],
    )
    assert log_group == ecs_seed["log_group"]


@pytest.mark.integration
def test_helpers_secret_read_and_update(secrets_client):
    secret_name = f"it-secret-{uuid.uuid4().hex[:8]}"
    original_secret = '{"token":"before"}'
    updated_secret = '{"token":"after"}'

    secrets_client.create_secret(Name=secret_name, SecretString=original_secret)
    fetched_secret = get_secret_value(profile="EC2_INSTANCE_METADATA", secret_name=secret_name)
    update_response = update_secret_string(
        profile="EC2_INSTANCE_METADATA",
        secret_name=secret_name,
        secret_string=updated_secret,
    )
    final_secret = secrets_client.get_secret_value(SecretId=secret_name)["SecretString"]

    assert fetched_secret == original_secret
    assert update_response["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert final_secret == updated_secret
