# Dictipy

Dictipy creates the right dict also for nested objects using recursion, whenever the standard
Python ```__dict__()``` cannot. 

![Python 2.7, 3.4, 3.5, 3.6, 3.7, 3.8](https://img.shields.io/badge/python-%202.7%2C%203.4%2C%203.5%2C%203.6%2C%203.7%2C%203.8-blue.svg)
[![PyPI version](https://badge.fury.io/py/dictipy.svg)](https://badge.fury.io/py/dictipy)
[![Build Status](https://travis-ci.org/gioelecrispo/dictipy.svg?branch=master)](https://travis-ci.org/gioelecrispo/dictipy)
[![codecov](https://codecov.io/gh/gioelecrispo/dictipy/branch/master/graph/badge.svg)](https://codecov.io/gh/gioelecrispo/dictipy)


## Table of contents
1. Motivation
2. Usage

## 1. Motivation
Using get_dict makes you able to recursively get dict of nested objects **without** explicitly 
overriding ```__repr__()``` function, making it usable for other purposes.
It could be useful when you have very complex nested object and you want not to override each sub-object 
```__repr__()``` function. Imagine for example an operation which produces a complex object which has to be
serialized and sent through a REST protocol as a json.
The ```json.dumps()``` cannot execute the task if the argument object is not a dict. Again, using simply the 
standard Python ```__dict__()``` function does not solve the problem if a nested object has to be considered.

## 2. Usage
Simply import ```get_dict``` function from ```dictipy``` and use it on any potentially serializable object.

---
Example 1: Nested objects.
```python
from dictipy import get_dict


class Parent:

    def __init__(self, parent_field):
        self.parent_field = parent_field
        self.child = Child(1)


class Child:

    def __init__(self, child_field):
        self.child_field = child_field


if __name__ == "__main__":
    p = Parent(0)
    print("Standard Python dict:  ", p.__dict__)
    print("Dictipy get_dict:      ", get_dict(p))
```

Result: 
```python
Standard Python dict:   {'parent_field': 0, 'child': <__main__.Child object at 0x0000021C530BFEB8>}
Dictipy get_dict:       {'parent_field': 0, 'child': {'child_field': 1}}
```

--- 
Example 2: Json serialization.
```python
from dictipy import get_dict
import json


class Parent:

    def __init__(self, parent_field):
        self.parent_field = parent_field
        self.child = Child(1)


class Child:

    def __init__(self, child_field):
        self.child_field = child_field


if __name__ == "__main__":
    p = Parent(0)
    j1 = json.dumps(p) # throws -> TypeError: Object of type Parent is not JSON serializable
    j2 = json.dumps(p.__dict__) # throws -> TypeError: Object of type Child is not JSON serializable
    j3 = json.dumps(get_dict(p)) # returns -> '{"parent_field": 0, "child": {"child_field": 1}}'
```
