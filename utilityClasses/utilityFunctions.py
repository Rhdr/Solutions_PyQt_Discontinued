import sys


def nz(value, noneReplacement):
    #mimic the access not zero function
    try:
        if value == None or value == "":
            return noneReplacement
        else:
            return value
    except:
        return noneReplacement