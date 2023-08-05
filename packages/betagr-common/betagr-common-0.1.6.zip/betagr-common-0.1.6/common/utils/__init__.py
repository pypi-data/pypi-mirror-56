from collections import namedtuple

def client_response(json={}, status=418, reason="I'm a teapot! forgot to pass reason!",
                    headers={'Content-Type': 'application\json'}, raw_content=b''):
    """Made in compatibility purpose only (defaults not implemented in namedtuple python <3.7)"""
    ClientResponse = namedtuple(typename='ClientResponse',
                                field_names='json status reason headers raw_content')

    return ClientResponse(json=json,
                          status=status,
                          reason=reason,
                          headers=headers,
                          raw_content=raw_content)
