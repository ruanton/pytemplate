import argparse
from pyramid.paster import bootstrap, setup_logging


def myfunction():
    parser = argparse.ArgumentParser(description='Description of myfunction.')
    parser.add_argument('config_uri', help='The URI to the configuration file.')
    args = parser.parse_args()

    setup_logging(args.config_uri)
    with bootstrap(args.config_uri) as env:
        settings = env['registry'].settings
        print('Registry settings:')
        for k, v in settings.items():
            print(f'{k} = {v}')
