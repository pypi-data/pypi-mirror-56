import os

_config_locations = [
    'conf/xdcs-agent.toml',
    'conf/xdcs-agent.conf',
    './conf/xdcs-agent.toml',
    './conf/xdcs-agent.conf',
]


def main():
    for config_loc in _config_locations:
        print('Checking location ' + config_loc + ' for configuration')
        if os.path.isfile(config_loc):
            print('Found in ' + config_loc)
