try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from .mqtt import MQTTClient

import random
import time
import os
import collections
import queue
import socket


def create_filename(tmp):
    filename = os.path.join(tmp, '{0}.pickle'.format(int(time.time() * 1000)))
    return filename

def checking_connection(connection):
    """
    :return: boolean True or False
    """
    if not connection:
        client = MQTTClient('TestConnection')
        if network() and client.checking():
            return True
        return False
    return True


def network(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False


def queue_to_deque(queue):
    """
    :param queue: <queue.Queue at 0x7fc715978278>
    :return: deque([{..},{..}])
    """
    deque = collections.deque()
    while not queue.empty():
        elem = queue.get_nowait()
        deque.append(elem)
    return deque


def deque_to_queue(deque):
    """
    :param deque: deque([{..},{..}])
    :return: <queue.Queue at 0x7fc715978278>
    """
    q = queue.Queue()
    for e in deque:
        q.put_nowait(e)
    return q


def create_dir(directory):
    """
    :param directory: /tmp/files
    :return: True
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
    except OSError as e:
        raise ValueError(e)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def instance_config(filename):
    """
    :param filename:
    :return: class config
    """
    config = ConfigParser(dict_type=AttrDict)
    try:
        config.read(filename)
        return config._sections
    except:
        return []


def emit_data_mock(payload=None, jwt=False):
    """
    :return: {
        'id': int(1),'timestamp': int(123123) ,
        'latitud': float(35.000), 'longitud': float(34.000)
    }
    """
    data = {}
    if payload:
        data.update(payload)
    data.update({
        'id': random.randrange(0, 100),
        'timestamp': int(time.time() * 1000),
        'latitud': float('41.%s' % random.randrange(360000, 450000)),
        'longitud': float('2.%s' % random.randrange(120000, 200000))
    })
    return data
