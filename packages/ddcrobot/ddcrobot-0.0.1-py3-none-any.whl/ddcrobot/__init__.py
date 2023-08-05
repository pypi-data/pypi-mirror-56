__version__ = '0.0.1'
"""Extensions to the 'distutils' for large or complex distributions"""

from AIserver import server
from AIserver import client
__metaclass__ = type
s = server.server()
c = client.client()
__all__ = [
    'client', 'server'
]
class server(object):

    @staticmethod
    def left(step):
        s.left(step)
        # print("向左转")

class client(object):

    @staticmethod
    def left(step):
        c.left(step)
