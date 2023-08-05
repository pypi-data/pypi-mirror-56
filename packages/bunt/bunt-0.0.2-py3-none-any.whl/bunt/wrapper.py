import atexit
import unittest
from random import randint
from traceback import print_exc
from typing import Optional, Iterable, Type, get_type_hints

from docker import DockerClient
from docker.models.containers import Container
from docker.models.networks import Network

from bunt.config import bunt_docker_network_id, bunt_cleanup_created_resources
from bunt.containers import ContainerConfiguration, ContainerConfigurationClientConnectable
from bunt.environment import Environment


class Bunt:
    def __init__(
            self,
            docker_client: Optional[DockerClient] = None,
            docker_network: Optional[Network] = None
    ):
        self.docker_client = docker_client or DockerClient.from_env()

        if docker_network:
            # Allow end user to override convention
            self.docker_network = docker_network
        elif bunt_docker_network_id is not None:
            # We are running in a CI and we are being told to use a very specific network
            self.docker_network = self.docker_client.networks.get(bunt_docker_network_id)
        else:
            # No network provided so default to some seperate network.
            self.docker_network = self.docker_client.networks.create(
                f'bunt-{randint(100, 999)}',
                driver='bridge'
            )

        atexit.register(self.cleanup)

    def main(self):
        print('Main')
        unittest.main()
        print('Finished')

    def cleanup(self):
        if bunt_cleanup_created_resources:
            # Kill and remove containers
            while len(self.docker_network.containers) > 0:
                container: Container
                for container in self.docker_network.containers:
                    # Remove from network
                    self.docker_network.disconnect(container)
                    # Remove
                    container.remove(v=True, force=True)

            # Remove network
            self.docker_network.remove()

        self.docker_client.close()

    def environment(self, container_configurations: Iterable[Type[ContainerConfiguration]]) -> Environment:
        return Environment(self.docker_client, self.docker_network, frozenset(container_configurations))

    def test_case(self, container_configurations: Iterable[Type[ContainerConfiguration]]):
        environment = self.environment(container_configurations)

        def environment_wrapper(test_case_function):

            def test_case_wrapper(*args, **kwargs):
                with environment:
                    # TODO: Make some kind of container wrapper and pass this to the test case function
                    type_hints = get_type_hints(test_case_function)
                    kwargs = {}

                    closing_required = []

                    for container_type, container in environment.containers.items():
                        for name, type_of_hint in type_hints.items():

                            # Check if this type specifies a special client connection type.
                            cc_type = issubclass(
                                container_type,
                                ContainerConfigurationClientConnectable
                            )

                            connection = None
                            if issubclass(container_type, type_of_hint):
                                connection = kwargs[name] = container_type(
                                    docker_client=self.docker_client,
                                    docker_network=self.docker_network,
                                    docker_container=container
                                )
                            elif cc_type and issubclass(container_type.connectable_container_type, type_of_hint):
                                connection = kwargs[name] = container_type.connection()

                            if connection is not None and hasattr(connection, 'close'):
                                closing_required.append(connection)

                    try:
                        return test_case_function(*args, **kwargs)
                    except Exception as e:
                        raise e
                    finally:
                        for connection in closing_required:
                            try:
                                connection.close()
                            except:
                                print_exc()
                                print('Failed to close', connection, '!!!')

            return test_case_wrapper

        return environment_wrapper
