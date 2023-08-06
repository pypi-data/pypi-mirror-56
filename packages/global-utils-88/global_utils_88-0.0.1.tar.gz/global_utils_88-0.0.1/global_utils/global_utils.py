import base64
import inspect
from datetime import datetime


dummy1, dummy2, dummy3 = [[1, 1, 3, 2, 0]], [
    [1, 1, 3, 0, 0]], [[0, -1, -6, -1, 1]]


def string_to_well_encoded_bytes(str):
    ''' Encode string to a well formed string of bytes'''
    str = str.encode('ISO-8859-1')
    return base64.b64decode(str)


def bytes_to_well_encoded_string(str):
    ''' Encode bytes to a well formed string, which can be accepted by the request library'''
    str = base64.b64encode(str)
    return str.decode("ISO-8859-1")


def read_from_file(file_):
    string = ''

    try:
        with open(file_, 'rb') as file:
            string = file.read()
    except IOError as err:
        print(err.args)
        print("ERROR, read_from_file. Filename: " + file_)
        string = "ERROR!"

    return string


def write_to_file(string_to_write, file_):

    with open(file_, 'wb') as file:
        file.write(string_to_write)


def getLineInfo():
    print("File: ", inspect.stack()[1][1], ":", "     Line: ", inspect.stack()[1][2], ":",
          inspect.stack()[1][3])


def rchop(thestring, ending1, ending2):
    if thestring.endswith(ending1):
        return thestring[:-len(ending1)]
    if thestring.endswith(ending2):
        return thestring[:-len(ending2)]
    return thestring


def get_timing(message, startTime):
    message_and_time = "||| " + str(message) + " ||| total time:" + str(datetime.now() - startTime)
    print(message_and_time)
    print("File: ", inspect.stack()[1][1], ":", "     Line: ", inspect.stack()[1][2], ":",
          inspect.stack()[1][3])
    return message_and_time
