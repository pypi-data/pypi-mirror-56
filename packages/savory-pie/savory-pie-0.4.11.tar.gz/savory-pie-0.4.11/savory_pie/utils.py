from datetime import datetime


def to_datetime(milliseconds):
    """
    Converts milliseconds in UTC (e.g., from JS `new Date().getTime()` into Python datetime
    """
    try:
        value = datetime.utcfromtimestamp(int(milliseconds) / 1000)
        if isinstance(value, datetime):
            return value
    except Exception:
        pass
    return milliseconds


def to_list(items):
    """
    Converts comma-delimited string into list of items
    """
    try:
        values = items.split(',')
        if isinstance(values, list):
            return values
    except Exception:
        pass
    return items


def get_exception_message(err):
    """
    Python 2 has the 'message' attribute for exceptions, however python 3 does not.  This helper method
    gives us the ability to sort out which one to use.
    :param err: Some exception
    :return: The exception message string
    """
    try:
        # python 2
        return err.message
    except AttributeError:
        # python 3
        return str(err)


class ParamsDict(object):
    """
    Simple class that wraps a dictionary and returns a list.
    This is used because filters support getting a list of values given a parameter,
    so when using a filter within a queryset, the filter (in the format of a dict)
    needs to support list related functions, this class acts a wrapper around the filter.

        Parameters:

            ``params``
                This is a dictionary of parameters
    """
    def __init__(self, params):
        self._params = params

    def keys(self):
        return self._params.keys()

    def __contains__(self, key):
        return key in self._params

    def __getitem__(self, key):
        if key in self._params:
            return self._params.get(key)
        else:
            raise KeyError

    def get(self, key, default=None):
        return self._params.get(key, default)

    def get_as(self, key, type, default=None):
        value = self._params.get(key, None)
        return default if value is None else type(value)

    def get_list(self, key):
        return [self._params[key]]

    def get_list_of(self, key, type):
        list = self._params.get(key, None)
        if list is None:
            return []
        else:
            return [type(x) for x in list]
