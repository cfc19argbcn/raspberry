import pickle
from collections import deque


def serialization_dump_obj(data, filename):
    """
    :param data: deque
    :param filename: '/tmp/dqueue/data.pickle'
    :return: True
    """
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return True
    except Exception as e:
        return False


def serialization_load_obj(filename):
    """
    :param filename:
    :return:
    """
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        return False
