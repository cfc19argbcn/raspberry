import pickle
from collections import deque


def serialization_dump_obj(data, filename):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return {'status': True}
    except Exception as e:
        raise ValueError(e)


def serialization_load_obj(filename):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        raise ValueError(e)


def serialization_sample():
    filename = '/tmp/dqueue/data.pickle'
    d = deque()
    for k in [{'id': 27,
               'timestamp': 1561896041777,
               'latitud': 41.377493,
               'longitud': 2.150057},
              {'id': 65,
               'timestamp': 1561896042268,
               'latitud': 41.421367,
               'longitud': 2.165555}]:
        d.append(k)
    response = serialization_dump_obj(d, filename)
    dequeu = serialization_load_obj(filename)
    if response['status']:
        print(dequeu)
