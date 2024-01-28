import json
from typing import Type

from pydantic import BaseModel
from requests import Response


class JsonParser:
    """
    Facade to parse different objects into json strings
    """

    _TYPE_TO_PARSER_FUNC = {
        Response: lambda r: r.text,
        str: lambda x: x,
        dict: json.loads,
    }

    @staticmethod
    def _parse_pydantic_model(x: Type[BaseModel]):
        return x.model_dump_json()

    @classmethod
    def loads(cls, x: Response | str | dict | Type[BaseModel]) -> str:
        """
        Convert the x into a proper json string from various types

        This is not as simple as json loads. We have python-native objects
        like requests.Response and Pydantic Models that all need to be
        converted to the standard json. This

        :param x: any value to convert into a json
        :return: the parsed json string
        """
        x_type = type(x)
        if x_type in cls._TYPE_TO_PARSER_FUNC:
            parse_func = cls._TYPE_TO_PARSER_FUNC[type(x)]
        elif isinstance(x, BaseModel):
            parser_func = cls._parse_pydantic_model

        return parse_func(x)
