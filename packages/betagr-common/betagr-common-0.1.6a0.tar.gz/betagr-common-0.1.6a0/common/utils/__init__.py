from collections import namedtuple


ClientResponse = namedtuple(typename='ClientResponse',
                            field_names=['json', 'status', 'headers', 'raw_content'],
                            defaults=[{}, 418, {'Content-Type'}, b''])
