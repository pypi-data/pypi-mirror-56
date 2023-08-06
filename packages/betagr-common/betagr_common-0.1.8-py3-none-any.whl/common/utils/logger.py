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
                        format='[%(asctime)s] - [%(levelname)s] [%(filename)s>%(lineno)d] - %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S')

    logging.info(f'Start logging client...\n'
                 f'Client {client.__class__.__name__} created with: '
                 f'polled server host: {client.url}, '
                 f'with default headers: {client.headers}.')
