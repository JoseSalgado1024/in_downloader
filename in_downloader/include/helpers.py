# -*- coding: utf-8 -*-


def guid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    from time import time
    from random import random
    import socket
    from hashlib import md5

    t = long(time() * 1000)
    r = long(random()*100000000000000000L)
    try:
        a = socket.gethostbyname(socket.gethostname())
    except:
        # if we can't get a network address, just imagine one
        a = random()*100000000000000000L
    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    data = md5(data).hexdigest()

    return data


def safty_name(where, name):
    from os.path import exists, join
    from os import mkdir

    if not isinstance(where, (unicode, str)) or not isinstance(where, (unicode, str)):
        raise TypeError('Tanto \'where\' como \'name\' deben ser instancias de STR o UNICODE.')
    if not exists(where):
        mkdir(where)
    name_pattern = '{name}_{count}'
    count = 0
    secure_path = join(where, name_pattern.format(name=name, count=count))
    while exists(secure_path):
        count += 1
        secure_path = (where, name_pattern.format(name=name, count=count))
    return secure_path


def resolve_kwargs(configs, _kwargs):
    """
    Función de renderizado de KWARGS

    Args:
        - defaults:
        - _kwargs:
    Return:
        - Dict.
    """
    if not isinstance(configs, dict) or not isinstance(_kwargs, dict):
        raise TypeError('Argumentos no validos.')
    _tmp_configs = {}
    for k, v in configs.items():
        if k in _kwargs.keys() and isinstance(_kwargs.get(k), v.__class__):
            if isinstance(v, dict):
                _tmp_configs.update({k: resolve_kwargs(v, _kwargs.get(k))})
            else:
                _tmp_configs.update({k: _kwargs[k]})
        else:
            _tmp_configs.update({k: v})
    return _tmp_configs


def atom_fetch_info(_url):
    """

    Return:
    """
    from requests import get
    from requests.exceptions import ConnectionError, ConnectTimeout
    if not isinstance(_url, (str, unicode)):
        raise TypeError('El argumento \'_url\' debe ser una instancia de STR o UNICODE.')
    metadata_img = {
        'format': 'unknown',
        'encoding': 'unknown',
        'status_code': 'unknown',
        'size': 0,
        'modified': 'unknown',
        'is_image': False,
        'msg': '',
        'mem_units': 'bytes',
        'url': _url,
    }
    image_formats = \
        [
            'image/jpeg',
            'image/png',
            'image/tiff',
        ]
    try:
        res = get(_url)
        metadata_img.update({
            'elapsed':  res.elapsed.total_seconds(),
            'msg':  'Ejecutado correctamente.',
            'encoding': res.encoding,
            'status_code': res.status_code,
            'is_image': True if res.headers.get('Content-Type', 'unknown') in image_formats else False,
            'format': res.headers.get('Content-Type', 'unknown'),
            'size': res.headers.get('Content-Length', 0),
            'modified': res.headers.get('Last-Modified', 'unknown')
        })
    except (ConnectionError, ConnectTimeout) as http_err:
        metadata_img.update({'msg': http_err})
    return metadata_img


def compile_string(string, options=None):
    """

    :param string:
    :param options:
    :return:
    """
    if not isinstance(string, (str, unicode)):
        raise TypeError('\'string\' debes ser una instancia de STR o UNICODE.')
    if not isinstance(options, dict):
        raise TypeError('\'options\' debes ser una instancia de STR o UNICODE.')
    for k, v in options.items():
        if isinstance(v, (str, unicode)):
            wildcard = '@{}'.format(k)
            if wildcard in string:
                string = string.replace(wildcard, v)
    return string