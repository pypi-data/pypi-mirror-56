# -*- coding: utf-8 -*-

"""
A simple python module to make transformations easy between json and python objects
"""
import json
from typing import Any

__author__ = 'ozgur'
__creation_date__ = '2.12.2019' '12:57'


class JsonObject:
    """
    A simple python object which can easily transform to and from json
    """

    def to_dict(self) -> dict:
        """
        returns data as dict\n
        :return: data
        """
        return self.__dict__.copy()

    def to_dict_compressed(self) -> dict:
        """
        returns data as dict and removes empty fields\n
        :return: data
        """
        retdict = dict((i, d) for i, d in self.to_dict().items() if d)
        return retdict

    def from_dict(self, updatedict: dict):
        """
        populates data from dict
        :param updatedict: dict which contains data
        :return: None
        """
        self.__dict__.update(updatedict.copy())

    def to_json(self) -> str:
        """
        returns data dict as json str\n
        :return: data
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    def to_json_compressed(self) -> str:
        """
        returns data dict as single linejson str, before that removes empty fields \n
        :return: data
        """
        return json.dumps(self.to_dict_compressed(), ensure_ascii=False)

    def from_json(self, jsontxt: str):
        """
        populates data from json dict
        :param jsontxt: str which contains data in json format
        :return: None
        """
        self.from_dict(json.loads(jsontxt, encoding="UTF-8"))

    def set_attribute_by_name(self, atrributename: str, value: Any):
        """
        Sets an attribute of the object if defined in class declaration, else raises AttributeError
        You must be sure that constructor must take no value. Otherwise it raises TypeError
        :param atrributename: attribute name to set
        :param value: value to set
        :raises AttributeError
        :return: None
        """
        if atrributename in self.__class__().__dict__:
            self.__dict__[atrributename] = value
        else:
            raise AttributeError(self.__class__.__name__, atrributename)
