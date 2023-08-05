from collections import namedtuple


ClientResponse = namedtuple(typename='ClientResponse',
                            field_names=['json', 'status', 'reason', 'headers', 'raw_content'],
                            defaults=[{}, 418, "I'm a teapot! forgot to pass reason!", {'Content-Type'}, b''])
