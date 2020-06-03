"""
__init__.py

TODO описание модуля

created by pavel in pavel as 5/29/20
Проект aicrawler
"""

import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v3"
__status__ = 'Development'
__version__ = '20200529'


from typing import Callable, List
from core import Info


class Filter:

    def __init__(self, *, func_rule: Callable, repr_str: str = None):  #  _list=None):
        self._func_rule = func_rule
        # if _list:
        #     self._list = _list
        # else:
        #     self._list = [func_rule]
        self._repr_str = repr_str if repr_str is not None else repr(func_rule)

    def __call__(self, message: Info) -> bool:
        return self._func_rule(message)

    def __invert__(self):

        def func_rule(message: Info) -> bool:
            return not self._func_rule(message)

        # _list = [['~'] + self._list]
        repr_str = '~' + self._repr_str
        return Filter(func_rule=func_rule, repr_str=repr_str)  # _list=_list)

    def __and__(self, other):
        assert isinstance(other, Filter)

        def func_rule(message: Info) -> bool:
            return self._func_rule(message) and other._func_rule(message)
        # _list = [(self._list + ['&']  + other._list)]
        repr_str = f'({self._repr_str}&{other._repr_str})'
        return Filter(func_rule=func_rule, repr_str=repr_str)  # _list=_list)

    def __or__(self, other):
        assert isinstance(other, Filter)

        def func_rule(message: Info) -> bool:
            return self._func_rule(message) or other._func_rule(message)
        # _list = [(self._list + ['|']  + other._list)]
        repr_str = f'({self._repr_str}&{other._repr_str})'
        return Filter(func_rule=func_rule, repr_str=repr_str)  # _list=_list)

    def __repr__(self):
        # repr_string = ''.join(el if isinstance(el, str) else repr(el) for el in self._list)
        return self._repr_str




