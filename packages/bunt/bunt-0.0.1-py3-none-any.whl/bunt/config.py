from docker import DockerClient
from os import getenv

docker_client = DockerClient.from_env()
bunt_docker_network_id = getenv('BUNT_NETWORK', None)
bunt_cleanup_created_resources = getenv('BUNT_CLEANUP_CREATED_RESOURCES', 'true') in ['true']
