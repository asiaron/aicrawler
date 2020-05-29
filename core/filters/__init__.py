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


from typing import Callable, Dict


class Filter(object):

    def __init__(self, *, func_rule: Callable, _list=None):
        self._func_rule = func_rule
        if _list:
            self._list = _list
        else:
            self._list = [func_rule]

    def __call__(self, message: Dict) -> bool:
        return self._func_rule(message)

    def __neg__(self):

        def func_rule(message: Dict) -> bool:
            return not self._func_rule(message)

        _list = [(['~'] + self._list)]
        return Filter(func_rule=func_rule, _list=_list)

    def __and__(self, other):
        assert isinstance(other, Filter)

        def func_rule(message: Dict) -> bool:
            return self._func_rule(message) and other._func_rule(message)
        _list = [(self._list + ['&']  + other._list)]
        return Filter(func_rule=func_rule, _list=_list)

    def __or__(self, other):
        assert isinstance(other, Filter)

        def func_rule(message: Dict) -> bool:
            return self._func_rule(message) or other._func_rule(message)
        _list = [(self._list + ['|']  + other._list)]
        return Filter(func_rule=func_rule, _list=_list)




