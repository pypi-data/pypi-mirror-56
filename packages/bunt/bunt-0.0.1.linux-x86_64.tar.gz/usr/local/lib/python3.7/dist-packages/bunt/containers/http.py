from urllib.parse import urljoin

import requests
from docker import DockerClient
from docker.models.containers import Container
from docker.models.networks import Network

from bunt.containers.configuration import ContainerConfiguration
from bunt.containers.health import ContainerConfigurationHealthCheck


class PrefixedSession(requests.Session):

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

        # Disable SSL Verification
        self.verify = False

    def request(self, method, url, *args, **kwargs):
        full_url: str = urljoin(self.base_url, url)
        return super().request(method, full_url, *args, **kwargs)


class ContainerConfigurationHttp(
    ContainerConfiguration,
):
    """
    :type ContainerConfiguration
    """
    http_protocol: str = 'http'  # Can be https
    http_port: int = 80

    def __init__(
            self,
            docker_client: DockerClient,
            docker_network: Network,
            docker_container: Container,
            *args, **kwargs
    ):
        super().__init__(
            docker_client=docker_client,
            docker_network=docker_network,
            docker_container=docker_container,
            *args,
            **kwargs
        )
        self.http_session: PrefixedSession = PrefixedSession(self.http_base_url())

    @classmethod
    def http_base_url(cls) -> str:
        return f'{cls.http_protocol}://{cls.host_name}:{cls.http_port}/'

    def close(self):
        self.http_session.close()


class ContainerConfigurationHttpHealthCheck(
    ContainerConfigurationHealthCheck
):
    http_health_check_path: str = '/healthz'
    http_health_check_acceptable_status_codes: int = [200, 201, 404]

    @classmethod
    def health_check(cls, **kwargs) -> bool:
        try:
            with requests.Session() as session:
                response = session.get(urljoin(cls.http_base_url(), cls.http_health_check_path))
                return response.status_code in cls.http_health_check_acceptable_status_codes
        except:
            return False
