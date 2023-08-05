# if the functionality would bee expanded, create a class instead

import logging
import os


def start_logging(client):
    """ Started logging process.
    :param client: BaseClient,
    :return: None
    """
    # see numeric represents level here: https://docs.python.org/3/library/logging.html#logging-levels
    logging_mode = os.getenv('COMMON_API_CLIENT_LOGGING_LEVEL', 40)  # Error by default

    logging.basicConfig(level=int(logging_mode),
                        format='[%(asctime)s] - [%(levelname)s] - %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S')

    logging.info('Start logging...')
    logging.info(f'Client {client.__class__.__name__} created:'
                 f' host - {client.url},'
                 f' headers - {client.headers}')
