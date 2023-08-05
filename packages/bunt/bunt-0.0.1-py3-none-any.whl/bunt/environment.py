import logging
from collections import deque
from time import sleep
from typing import FrozenSet, Dict, Type, Iterable

from docker.client import DockerClient
from docker.errors import NotFound, APIError
from docker.models.containers import Container
from docker.models.networks import Network

from bunt.containers import ContainerConfiguration
from bunt.containers import ContainerConfigurationHealthCheck
from bunt.exceptions import ContainerNeverBecameHealthy


class ConfigurationOrderer:
    """
    Order an iterable of configs so that the containers they create will start in the correct order.
    """

    def __init__(self, container_configurations: Iterable[Type[ContainerConfiguration]]):
        self.container_configurations = container_configurations

    def flattened(self):
        queue = deque(self.container_configurations)
        seen = set()

        while queue:
            config = queue.pop()

            # Do we have our own deps?
            if config.depends_on:
                for dep in config.depends_on:
                    if dep not in seen:
                        queue.appendleft(dep)

            # Don't return the same thing twice
            if config in seen:
                continue

            yield config
            seen.add(config)

    def __iter__(self):
        started = set()
        remaining = set(self.flattened())

        while remaining:
            # Find all containers we can now start
            startable = {
                config
                for config in remaining
                if all(dep in started for dep in config.depends_on)
            }

            # Start them
            yield from startable
            started = started.union(startable)
            remaining = remaining - startable


class Environment:
    def __init__(
            self,
            docker_client: DockerClient,
            docker_network: Network,
            container_configurations: FrozenSet[Type[ContainerConfiguration]],
            cleanup_network: bool = False
    ):
        self.docker_client = docker_client
        self.docker_network = docker_network
        self.container_configurations = list(ConfigurationOrderer(container_configurations))
        self.containers: Dict[Type[ContainerConfiguration], Container] = {}
        self.cleanup_network = cleanup_network

    def wait_for_healthy(self, container_configuration: Type[ContainerConfigurationHealthCheck], container: Container):
        """
        Wait for a container to be healthy
        :param container_configuration:
        :param container:
        :return:
        """

        wait = container_configuration.health_check_time_out / container_configuration.health_check_maximum_retries
        for i in range(container_configuration.health_check_maximum_retries):
            try:
                if container_configuration.health_check(container=container):
                    return True
            except:
                logging.exception(f'Health check of {container_configuration.name} failed', exc_info=True)
            sleep(wait)
        return False

    def deploy(self, container_configuration: Type[ContainerConfiguration]) -> Container:
        volumes = [
            f'{src}:{dst}:rw'
            for src, dst in container_configuration.volume_mounts.items()
        ]

        # Create a container
        container = self.docker_client.containers.create(
            image=container_configuration.image,

            # Labeling and tagging this container
            name=container_configuration.name,
            hostname=container_configuration.host_name,

            # Configuring the application in this container
            environment=container_configuration.environment_variables,
            entrypoint=container_configuration.entry_point,
            command=container_configuration.command,

            ports={
                port_string: None
                for port_string in [f'{p}/tcp' for p in container_configuration.tcp_ports]
            },

            volumes=volumes,

            # Performance tweaking for container creation and teardown
            # stop_timeout=1,
            detach=True,
        )

        # Make it discoverable by it's hostname
        self.docker_network.connect(container, aliases=[
            container_configuration.host_name
        ])

        return container

    def start(self, config: Type[ContainerConfiguration], container: Container):
        """
        Start a container and run through startup checks
        :param config:
        :param container:
        :return:
        """
        container.start()

        if issubclass(config, ContainerConfigurationHealthCheck):
            if not self.wait_for_healthy(config, container):
                raise ContainerNeverBecameHealthy(f'{config.name} failed to become healthy')

    def __careful_remove_container(self, container: Container):
        try:
            container.remove(
                v=True,
                force=True
            )
        except NotFound:
            return
        except APIError as e:
            if e.status_code != 409:
                # Error code 409 means...
                #   removal of container $ID is already in progress
                # ...so we can ignore these. If the error code is not
                # a 409 it may be important!
                raise e

        try:
            container.wait(condition='removed')
        except NotFound:
            pass

    def stop(self, config: Type[ContainerConfiguration], container: Container):
        """
        Stop a container and run through shutdown checks
        :param config:
        :param container:
        :return:
        """
        self.__careful_remove_container(container)

    def __enter__(self):
        for container_configuration in self.container_configurations:
            container = self.deploy(container_configuration)
            self.containers[container_configuration] = container
            self.start(container_configuration, container)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for config in reversed(self.container_configurations):
            container = self.containers[config]
            # Destroy all managed containers
            self.stop(config, container)
            self.__careful_remove_container(container)
            del self.containers[config]
