from typing import List, Optional, Union, IO, Type, Iterable

from bunt.containers.http import ContainerConfigurationHttp
from bunt.exceptions import ContainerRestStyleException, ContainerRestException, ContainerRestNotFound

RestResponseType = Optional[Union[List[dict], dict, str, float, int]]


def restful_pedantic_convention_enforcement(
        singular_resource: Optional[bool] = None,
        expects_list: Optional[bool] = None
):
    def wrapper(function):
        def handler(self, path: Union[Iterable, str], **kwargs):
            if self.rest_styling_pedantic:

                if isinstance(path, str):
                    is_even = (len(path.strip('/').split('/')) % 2) == 0
                else:
                    path = list(path)
                    is_even = (len(path) % 2) == 0

                if singular_resource is None:
                    # Ignore this check
                    pass
                elif singular_resource and not is_even:
                    raise ContainerRestStyleException(
                        'RESTful APIs that retrieve an object should end with an ID following a '
                        'http://server/<type>/<id>/<type>/<id> pattern.'
                    )
                elif not singular_resource and is_even:
                    raise ContainerRestStyleException(
                        'RESTful APIs that list a collection should not end with an ID and should follow a '
                        'http://server/<type>/<id>/<type>/<id> pattern.'
                    )

            response: RestResponseType = function(self, path, **kwargs)

            if self.rest_styling_pedantic:
                if expects_list is None:
                    # If we don't want to do this check, ignore it.
                    pass
                elif not expects_list and not isinstance(response, dict):
                    raise ContainerRestStyleException(
                        f"RESTful APIs should return dict when fetching a singular resource, not {type(response)}."
                    )
                elif expects_list and not isinstance(response, list):
                    raise ContainerRestStyleException(
                        f"RESTful APIs should return lists when fetching a collection, not {type(response)}."
                    )

            return response

        return handler

    return wrapper


class ContainerConfigurationRest(
    ContainerConfigurationHttp,
):
    rest_styling_pedantic: bool = True

    def __url(self, parts: Union[Iterable, str]) -> str:
        if isinstance(parts, str):
            path = parts
        else:
            path = '/'.join((
                part.rstrip('/') for part in parts
            ))
        return path.strip('/')

    def request(
            self,
            method: str,
            path: Union[Iterable, str], *,
            params: Optional[dict] = None,
            body: Optional[Union[str, bytes, bytearray, IO]] = None,
            json: Optional = None,
            parse_json: bool = True,
            **kwargs
    ):
        """
        Handle a request
        :param method: "GET", "POST", "PUT", "HEAD", "DELETE"
        :param path: Iterable[str]
        :param params: Optional[dict]
        :param body: Optional[Union[str, bytes, bytearray, IO]]
        :param json: Optional[RestResponseType]
        :param parse_json: If True we automatically parse the contents of the response as JSON
        :return: RestResponseType
        """

        if self.rest_styling_pedantic:
            if method not in ["GET", "POST", "PUT", "HEAD", "DELETE"]:
                raise ContainerRestStyleException(
                    'The RESTful HTTP methods are "GET", "POST", "PUT", "HEAD", "DELETE"'
                )

            if method in ['DELETE', 'GET', 'HEAD'] and (body is not None or json is not None):
                raise ContainerRestStyleException(
                    f'RESTful {method} requests should not contain bodies'
                )

            if method in ['DELETE', 'PUT', 'POST'] and (params is not None):
                raise ContainerRestStyleException(
                    f'RESTful {method} requests should not contain query parameters'
                )

        safe_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in {'url', 'params', 'data', 'json', 'parse_json', 'method', 'path', 'body'}
        }
        requests_arguments = {
            **safe_kwargs,
            'url': self.__url(path),
            'params': params,
            'data': body,
            'json': json,
        }

        response = self.http_session.request(
            method,
            **requests_arguments
        )

        # Handle failed HTTP requests by throwing an exception.
        if not response:
            for sub_type in ContainerRestException.__subclasses__():
                sub_type: Type[ContainerRestException] = sub_type  # Adding type hinting
                if sub_type.status_code == response.status_code:
                    raise sub_type(response)
            else:
                # Some unknown status code was returned. Throw a generic exception
                raise ContainerRestException(response)

        if parse_json:
            return response.json()
        else:
            return response.content

    @restful_pedantic_convention_enforcement(singular_resource=False, expects_list=False)
    def create(self, path: Union[Iterable, str], body: Optional[Union[str, bytes, bytearray, IO]] = None,
               json: Optional[RestResponseType] = None) -> RestResponseType:
        """
        Create a restful object
        :param path: Iterable[str]
        :param body: Optional[Union[str, bytes, bytearray, IO]]
        :param json: Optional[RestResponseType]
        :return: RestResponseType
        """
        return self.request('POST', path=path, body=body, json=json)

    @restful_pedantic_convention_enforcement(singular_resource=False, expects_list=True)
    def list(self, path: Union[Iterable, str], params: Optional[dict] = None) -> RestResponseType:
        """
        List a restful object
        :param path: Union[Iterable, str]
        :param params: Optional[dict]
        :return: RestResponseType
        """
        return self.request('GET', path=path, **params)

    @restful_pedantic_convention_enforcement(singular_resource=True, expects_list=False)
    def get(self, path: Union[Iterable, str], params: Optional[dict] = None) -> RestResponseType:
        """
        Get a restful object
        :param path: Union[Iterable, str]
        :param params: Optional[dict]
        :return: RestResponseType
        """
        return self.request('GET', path=path, params=params)

    @restful_pedantic_convention_enforcement(singular_resource=True, expects_list=False)
    def update(
            self, path: Union[Iterable, str],
            body: Optional[Union[str, bytes, bytearray, IO]] = None,
            json: Optional[RestResponseType] = None
    ) -> RestResponseType:
        """
        Update a restful object
        :param path: Union[Iterable, str]
        :param body: Optional[Union[str, bytes, bytearray, IO]]
        :param json: Optional[RestResponseType]
        :return: RestResponseType
        """
        return self.request('PUT', path=path, body=body, json=json)

    @restful_pedantic_convention_enforcement(
        singular_resource=True,
    )
    def delete(self, path: Union[Iterable, str]) -> RestResponseType:
        """
        Delete a restful object
        :param path: Union[Iterable, str]
        :return: RestResponseType
        """
        return self.request('DELETE', path=path)

    @restful_pedantic_convention_enforcement(
        singular_resource=True,
    )
    def exists(self, path: Union[Iterable, str]) -> bool:
        """
        Check if a restful object exists
        :param path: Union[Iterable, str]
        :return: bool
        """
        try:
            self.request('HEAD', path=path, parse_json=False)
            return True
        except ContainerRestNotFound:
            return False
