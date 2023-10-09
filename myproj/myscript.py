import argparse
import logging
from pyramid.paster import bootstrap, setup_logging
from pyramid_zodbconn import get_connection
from pyramid.registry import Registry
from pyramid.request import Request
from ZODB.Connection import Connection

# local imports
from .settings import settings
from .models import get_app_root

log = logging.getLogger(__name__)


def myfunction():
    parser = argparse.ArgumentParser(description='Description of myfunction.')
    parser.add_argument('config_uri', help='The URI to the configuration file.')
    args = parser.parse_args()

    # setup logging from config file settings
    setup_logging(args.config_uri)

    # bootstrap Pyramid environment to get configuration
    with bootstrap(args.config_uri) as env:
        registry: Registry = env['registry']
        request: Request = env['request']

        print('Registry settings:')
        for k, v in registry.settings.items():
            print(f'{k} = {v}')

        print(f'\nAccess to custom_myproj_parameter = {settings.custom_myproj_parameter}')

        log.info('get database connection and App Root object')
        conn: Connection = get_connection(request)
        app_root = get_app_root(conn)
        _ = app_root


if __name__ == '__main__':
    myfunction()
