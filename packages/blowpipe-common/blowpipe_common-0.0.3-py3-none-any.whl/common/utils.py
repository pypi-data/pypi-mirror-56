import os
import sys
import socket


def get_free_port(low_port: int, high_port: int) -> int:
    """
    returns a free port in the range low,high
    :param low_port:
    :param high_port:
    :return:
    """
    current = low_port
    while current <= high_port:
        if is_port_available("0.0.0.0", current):
            return current
        current += 1
    return -1;


def is_port_available(host: str, port: int) -> bool:
    import socket
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            return False
        else:
            return True
    finally:
        if sock is not None:
            sock.close()


def resolve_file(candidate):
    """
    token switches any environment variables and ~ out of a string
    """
    tokens = os.environ
    return token_switch(candidate, tokens)


def token_switch(candidate, tokens):
    """
    tokens switches ${TOKEN} and $TOKEN values out of the
    candidate string using the dict of tokens passed
    :param candidate:
    :param tokens:
    :return:
    """
    keys = tokens.keys()
    candidate = candidate.replace("~", os.getenv("HOME"))
    for key in keys:
        token_value = tokens.get(key)
        token_key = "${" + key + "}"
        # print("candidate=" + candidate, ", token_key=" + token_key + ", token_value=" + token_value)
        candidate = candidate.replace(token_key, token_value)
        token_key = "$" + key + ""
        candidate = candidate.replace(token_key, token_value)
    return candidate


def list_tokens(candidate):
    """
    returns all occurrences of ${xxxxx}
    :param candidate:
    :param tokens:
    :return:
    """
    import re
    token_regex = "\$\{.*\}"
    c = re.compile(token_regex)
    p = c.findall(candidate)
    return []


def split_file(candidate) -> (str, str):
    """
    returns the directory path and the filename with no path information
    :param candidate:
    :return:
    """
    abs_file = resolve_file(candidate)
    filename = abs_file.split("/")[-1]
    index = len(filename)+1
    dirname = abs_file[0:-index]
    return dirname, filename


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()