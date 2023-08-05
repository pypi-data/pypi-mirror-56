from abc import ABC, abstractmethod
from typing import Type, Optional


class ContainerConfigurationClientConnectable(ABC):
    connectable_container_type: Optional[Type] = None

    @classmethod
    @abstractmethod
    def connection(cls, **kwargs):
        """
        Health check a container
        :return: A connection to the container
        """
