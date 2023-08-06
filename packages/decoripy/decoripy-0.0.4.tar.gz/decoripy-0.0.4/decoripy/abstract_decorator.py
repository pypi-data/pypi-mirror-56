"""
abstract_decorator.py
====================================
The main module
"""
from functools import partial
from abc import ABCMeta


class AbstractDecorator:
    """
        AbstractDecorator is a base class that has to be inherited by the newer
        classes implementing decorators. It provides a template built upon the
        basic wrapping of a function, hiding the implementation details, and
        providing some useful advantages:
            - no distinction between decorator with or without arguments has to
              be done;
            - a temporal based execution is provided.
        As regards the first point, the construct is generalized with the *args,
        **kwargs template, and the following statements apply:
        *args
            If the decorator is used on a function without parameters then
            the first args will be the function itself; decorators args and
            kwargs will be None. If, instead, the decorator is used with
            parameters, the unnamed parameters will be stored in args.
        *kwargs
            If the decorator is used on a function without parameters then
            decorators args and kwargs will be None. If, instead, the decorator
            is used with parameters, the named parameters will be
            stored in kwargs and accessible with the convention
            self.{name_of_param}, e.g. self.timeout.
        For the second point, the temporal base execution is provided through
        the overriding of the following methods:
            - ```do_before```
            - ```do```
            - ```do_after```.
    """

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        if args and callable(args[0]):
            self.function = args[0]
            self.args = None
            self.kwargs = None
        else:
            self.function = None
            self.args = args
            self.kwargs = kwargs
            self.__set_kwargs__()
        self.before_result = None
        self.execution_result = None
        self.after_result = None

    def __call__(self, *args, **kwargs):
        if args and callable(args[0]):
            self.function = args[0]

            def wrapper(*func_args, **func_kwargs):
                return self.__execute_function__(*func_args, **func_kwargs)
            return wrapper
        else:
            return self.__execute_function__(*args, **kwargs)

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __execute_function__(self, *func_args, **func_kwargs):
        self.before_result = self.do_before(*func_args, **func_kwargs)
        self.execution_result = self.do(*func_args, **func_kwargs)
        self.after_result = self.do_after(*func_args, **func_kwargs)
        return self.execution_result

    def __set_kwargs__(self):
        for key, value in self.kwargs.items():
            setattr(self, key, self.kwargs[key])

    def do_before(self, *args, **kwargs):
        """
            do_before
            Parameters
            ---------
            *args
                unnamed args of the decorated function. They can be accessed in
                order using the following syntax: args[0], args[1], etc.
            *kwargs
                named args of the decorated function. They can be accessed using
                the following syntax: kwargs[name_of_decorated_func_param]

             Returns
             --------
                the result of the before phase stored in self.before_result
            """
        pass

    def do(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def do_after(self, *args, **kwargs):
        pass
