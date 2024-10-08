from time import sleep
import random


def email_delay():
    sleep(random.uniform(2, 5))

def get_obj_attrs(obj):
    return {k: v for k, v in obj.__dict__.items() if not k.startswith("__")}

def get_obj_attr(obj, attr):
    for obj in [obj] + obj.__class__.mro():
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    raise AttributeError

def get_cls_attr(cls, attr):
    for cls in [cls] + cls.mro():
        if attr in cls.__dict__:
            return cls.__dict__[attr]
    raise AttributeError

def to_title_case_2(s):
    return s.replace("_", " ").title().replace(" ", "")
