from abc import ABC, abstractmethod


class ContainerConfigurationHealthCheck(ABC):
    # Maximum number of times we hit the healthcheck endpoint
    health_check_maximum_retries: int = 60
    # How long to wait for this service to become healthy before deciding it is dead
    health_check_time_out: float = 10

    @classmethod
    @abstractmethod
    def health_check(cls, **kwargs) -> bool:
        """
        Health check a container
        :return:
        """
