import datetime


def log(level, message, file_name=None):
    """Log messages to stdout or file
    TODO : Add file support

    This method will log messages from script

    Levels :
        0 -> ERROR
        1 -> WARNING
        2 -> NOTICE
        3 -> INFO
    """
    if file_name is None:
        print(message)
    else:
        pass


def chop_microseconds(delta):
    return delta - datetime.timedelta(
        microseconds=delta.microseconds
    )
