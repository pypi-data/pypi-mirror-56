import datetime


def number(variable, variable_name):
    if type(variable) != type(1):
        raise Exception("Invalid data. " + variable_name + " must be an integer")


def string(variable, variable_name):
    if type(variable) != type("a"):
        raise Exception("Invalid data. " + variable_name + " must be a string")


def datetimestring(variable, variable_name):
    if type(variable) != type(datetime.datetime.now()):
        raise Exception("Invalid data. " + variable_name + " must be a valid datetime string")

