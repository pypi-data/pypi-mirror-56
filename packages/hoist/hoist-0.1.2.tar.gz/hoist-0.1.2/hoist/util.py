import argparse
from typing import Dict, Any

import toml
import socket
from contextlib import closing


def load_config(path: str) -> Dict:
    with open(path) as f:
        return toml.load(f)


def parse_args() -> Dict[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='*', default=['hoist.main'], help='The command(s) to execute')
    parser.add_argument('--hoist-file', '-f', default='hoist.toml', help='The TOML file containing hoist commands')
    parser.add_argument('--hoist-addr', '-a', default='localhost', help='Websockets host name to bind to')
    parser.add_argument('--hoist-port', '-p', default=0, help='Websockets port to bind to')

    parsed, unknown = parser.parse_known_args()

    for arg in unknown:
        if arg.startswith(('-', '--')):
            parser.add_argument(arg)

    variables = vars(parser.parse_args())
    if variables['hoist_port'] == 0:
        variables['hoist_port'] = find_free_port()

    return variables


def nested_keys(dictionary: Dict, key_path: str) -> Any:
    keys = key_path.split('.')
    for key in keys:
        try:
            dictionary = dictionary[key]
        except KeyError:
            return None
    return dictionary


def find_free_port():
    """ https://stackoverflow.com/a/45690594 """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
