"""
Encoders for translating a dict graphql response into another form
"""
import json
from typing import List, Optional, Union, Type

from dacite import from_dict, Config

__all__ = ["dataclass_encoder", "json_encoder", "dict_encoder"]


def dataclass_encoder(
    call_base: str, response: Union[List[dict], dict], response_cls: Type[type]
) -> Optional[Union[List[type], type]]:
    """
    Response encoder that produces a list or a single instance of the response class
    :param call_base: The base query or mutation the response is coming from
    :param response: The dict response from the graphql server
    :param response_cls: The dataclass that was used to specify the response
    :return: An instance or list of instances of the response_cls instantiated with the graphql server response
    """
    if response_cls is None:  # no response was desired
        return
    response = response[call_base]  # index into the payload of the response for the call
    # Don't use dacite type checking, rely on pydantic dataclass for type checking if desired
    from_dict_config = Config(check_types=False)
    if isinstance(response, list):
        encoded_response = [from_dict(response_cls, row, from_dict_config) for row in response]
    else:
        encoded_response = from_dict(response_cls, response, from_dict_config)
    return encoded_response


def json_encoder(
    call_base: str, response: Union[List[dict], dict], response_cls: Type[type]
) -> str:
    """
    Response encoder that produces json string
    :param call_base: The base query or mutation the response is coming from
    :param response: The dict response from the graphql server
    :param response_cls: The dataclass that was used to specify the response
    :return: A json formatted string of the dict response
    """
    return json.dumps(response)


def dict_encoder(
    call_base: str, response: Union[List[dict], dict], response_cls: type
) -> Union[List[dict], dict]:
    """
    Default encoder which returns the response as a dict or list of dicts
    :param call_base: The base query or mutation the response is coming from
    :param response: The dict response from the graphql server
    :param response_cls: The dataclass that was used to specify the response
    :return: A json formatted string of the dict response
    :raises EncoderError:
    """
    if isinstance(response, (dict, list)):
        return response
    raise TypeError("response parameter is expected to be a dict or list")
