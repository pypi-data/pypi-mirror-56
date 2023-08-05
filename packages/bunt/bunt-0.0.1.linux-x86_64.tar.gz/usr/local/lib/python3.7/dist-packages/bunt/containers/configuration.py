from abc import ABC

from typing import Dict, Optional, List, FrozenSet, Type

from docker import DockerClient
from docker.models.containers import Container
from docker.models.networks import Network


class ContainerConfiguration:
    name: str = None
    image: str
    host_name: str
    environment_variables: Dict[str, str] = {}
    volume_mounts: Dict[str, str] = {}
    entry_point: Optional[List[str]] = None
    command: Optional[List[str]] = None

    tcp_ports: FrozenSet[int] = frozenset()

    depends_on: Optional[FrozenSet[Type['ContainerConfiguration']]] = frozenset()

    def __init__(
            self,
            docker_client: DockerClient,
            docker_network: Network,
            docker_container: Container,
            *args,
            **kwargs
    ):
        """
        Base configuration that bags up important variables for test case injection.
        :param docker_client:
        :param docker_network:
        :param docker_container:
        """
        self.docker_client: DockerClient = docker_client
        self.docker_network: Network = docker_network
        self.docker_container: Container = docker_container
