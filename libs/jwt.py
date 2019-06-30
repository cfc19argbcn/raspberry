import jwt
from datetime import datetime, timedelta


def encode(payload, config):
    """
    :param payload: {'test':'test1'}
    :param config: config.JWT
    :return: {'token': '..yJ0eXAiOiJKV1QiLCJhbGciOiJ-..'}
    """
    jwt_algorithm = config.get('jwt_algorithm')
    jwt_secret = config.get('jwt_secret')
    jwt_exp_delta = config.get('jwt_exp_delta_seconds')
    payload.update({'exp': datetime.utcnow() + timedelta(seconds=int(jwt_exp_delta))})
    jwt_token = jwt.encode(payload, jwt_secret, jwt_algorithm)
    return {'token': jwt_token.decode('utf-8')}


def decode(jwt_token, config):
    """
    :param jwt_token: '..yJ0eXAiOiJKV1QiLCJhbGciOiJ-..'
    :param config: config.JWT
    :return: {'message': 'success','payload': {'test': 'asasdasdd', 'exp': 1561887974}, 'status': 200}
    """
    if jwt_token:
        jwt_algorithm = config.get('jwt_algorithm')
        jwt_secret = config.get('jwt_secret')
        try:
            payload = jwt.decode(jwt_token, jwt_secret, algorithms=[jwt_algorithm])
            return {'message': 'success', 'payload': payload, 'status': 200}
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {'message': 'Signature has expired', 'status': 400}


def sample():
    """
    In [53]: decode(jwt_token['token'], config.JWT)
    Out[53]:
    {'message': 'success',
     'payload': {'test': 'asasdasdd', 'exp': 1561887974},
     'status': 200}

    """
    from utils import instance_config
    config = instance_config('../config.ini')
    jwt_token = encode({'test': 'asasdasdd'}, config.JWT)
    payload = decode(jwt_token['token'], config.JWT)
    print(payload)
