# Decoripy
decoripy provides a well-structured template class for creating Python decorators. It uses inheritance to be efficient 
and simple.

![Python 2.7, 3.5, 3.6, 3.7](https://img.shields.io/badge/python-%203.3%2C%203.4%2C%203.5%2C%203.6%2C%203.7-blue.svg)
[![PyPI version](https://badge.fury.io/py/decoripy.svg)](https://badge.fury.io/py/decoripy)
[![Build Status](https://travis-ci.org/gioelecrispo/decoripy.svg?branch=master)](https://travis-ci.org/gioelecrispo/decoripy)

## Table of contents
1. Motivation
2. Usage

## 1. Motivation
With decoripy, writing a decorator becomes very easy. It aims to improve the Python language expressiveness by 
enhancing a very powerful Python mechanism.

Decoripy provides a template built upon the basic wrapping of a function, hiding the implementation details, and
providing some useful advantages:
 - no distinction between decorator with or without arguments has to be done;
 - a temporal based execution is provided. 

### Decorator arguments
With decoripy you could create decorator with or without arguments with no pain.
In standard Python you should handle the arguments passed to the decorator, because, in this case, the wrapper 
function does not take the function as a the first argument.
So you could do something like this:
```python
@MyDecorator
def function_to_decorate(var):
    pass
```
or 
```python
@MyDecorator(True)
def function_to_decorate(var):
    pass
```
or 
```python
@MyDecorator(timeout=3000, num_retries=3)
def function_to_decorate(var):
    pass
```
or 
```python
@MyDecorator(True, timeout=3000, num_retries=3)
def function_to_decorate(var):
    pass
```
and you have not to change your code. 
The unnamed arguments (```*args```) passed to the decorator can be accessed by using the positional order (For example, 
the first parameters could be taken in this way: ```first_arg = args[0]```, see Usage).
The named arguments (```**kwargs```) passed to the decorator are parsed and can be accessed by their name (For example, 
timeout could be used in the implementation code in this way: ```self.timeout```, see Usage).


### Temporal based execution
The decoripy template is built to provide temporal based execution:
 - you could execute a pre-operation **before** the decorated function is executed;
 - you could do some operation **while** the decorated function is executed;
 - you could execute a post-operation **after** the decorated function is executed.

In this way you can control the execution flow of the decorated function.

### Nested decorator
You could nest more decorator. The order respects the writing order, so:
 ```python
@First(timeout=3000)
@Second
def function_to_decorate(var):
    pass
```
@First is executed before; 
 
## 2. Usage
In order to create a new decorator, you have only to write a new class inheriting from the
abstract class AbstractDecorator, and overriding the following (optional) methods:
 - ```__do_before__```: 
 - ```__do__```: it is mandatory doing the ```self.function(*args, **kwargs)``` call here to trigger the
 decorated function execution.
 - ```__do_after__```:


The overriding of the three functions is optional. Clearly, no overriding means no
operations done upon the decorated function.
Summarizing, you have only to handle the temporal phases you are interested on.
 
---
 
Example 1 - No decorator arguments:

```python
from decoripy import AbstractDecorator


class DecoratorWithoutArguments(AbstractDecorator):
    
    def __do_before__(self, *args, **kwargs):
        print("Executing: __do_before__")
        return "Executed: __do_before__"

    def __do__(self, *args, **kwargs):
        print(self.before_result, ", Executing: __do__")
        function_result = self.function(*args, **kwargs)
        return function_result + ", Executed: __do__"

    def __do_after__(self, *args, **kwargs):
        print(self.execution_result, ", Executing: __do_after__")
        return "Executed: __do_after__"


@DecoratorWithoutArguments
def function_to_decorate(var1, var2, dict_var1, dict_var2):
    print("Executing: function: ", var1, var2, dict_var1, dict_var2)
    return "Executed: function"


function_to_decorate(1, "var2", dict_var1=[1, 2, 3], dict_var2={"key": "value"})
```

