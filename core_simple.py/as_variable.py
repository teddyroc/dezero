from tkinter import Variable


def as_variable(obj):
    if isinstance(obj, Variable):
        return obj
    return Variable(obj)