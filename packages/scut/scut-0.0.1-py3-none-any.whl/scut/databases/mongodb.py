import socket
from ctypes import c_int

from bunt.containers import ContainerConfiguration
from bunt.containers import ContainerConfigurationClientConnectable
from bunt.containers import ContainerConfigurationHealthCheck

try:
    from pymongo import MongoClient
except:
    MongoClient = None

# OP_QUERY: {
#    'flags': 0,
#    'fullCollectionName': b'admin.$cmd',
#    'numberToSkip': 0,
#    'numberToReturn': 1,
#    'query': {
#        'isMaster': 1,
#        'client': {
#            'application': {
#                'name': 'MongoDB Shell'
#            },
#            'driver': {
#                'name':
#                'MongoDB Internal Client',
#                'version': '3.4.4'
#            },
#            'os': {
#                'type': 'Windows'$
#                'name': 'Microsoft Windows 8',
#                'architecture': 'x86_64',
#                'version': '6.2 (build 9200)'
#            }
#        }
#    }
# }
PAYLOAD = b'#\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd4\x07\x00\x00\x00\x00\x00\x00admin.$cmd\x00\x00\x00\x00' \
          b'\x00\x01\x00\x00\x00\xfc\x00\x00\x00\x10isMaster\x00\x01\x00\x00\x00\x03client\x00\xe1\x00\x00\x00' \
          b'\x03application\x00\x1d\x00\x00\x00\x02name\x00\x0e\x00\x00\x00MongoDB ' \
          b'Shell\x00\x00\x03driver\x00:\x00\x00\x00\x02name\x00\x18\x00\x00\x00MongoDB Internal ' \
          b'Client\x00\x02version\x00\x06\x00\x00\x003.4.4\x00\x00\x03os\x00l\x00\x00\x00\x02type\x00\x08\x00\x00' \
          b'\x00Windows\x00\x02name\x00\x14\x00\x00\x00Microsoft Windows ' \
          b'8\x00\x02architecture\x00\x07\x00\x00\x00x86_64\x00\x02version\x00\x11\x00\x00\x006.2 (build ' \
          b'9200)\x00\x00\x00\x00'


class MongoContainer(
    ContainerConfiguration,
    ContainerConfigurationHealthCheck,
    ContainerConfigurationClientConnectable
):
    """
    Start an ephemeral MongoDB instance within your testing environment.
    """
    name = 'mongo'
    host_name = 'mongo'

    image = 'mongo:4.2.1'

    tcp_ports = frozenset({
        27017
    })

    environment_variables = {
        'MONGO_INITDB_ROOT_USERNAME': 'root',
        'MONGO_INITDB_ROOT_PASSWORD': 'root'
    }

    connectable_container_type = MongoClient

    @classmethod
    def connection(cls, **kwargs):
        if MongoClient is None:
            raise RuntimeError('Mongo driver is not installed. Please install pymongo.')

        username = cls.environment_variables['MONGO_INITDB_ROOT_USERNAME']
        password = cls.environment_variables['MONGO_INITDB_ROOT_PASSWORD']
        return MongoClient(f'mongodb://{username}:{password}@{cls.host_name}:27017')

    @classmethod
    def health_check(cls, **kwargs) -> bool:
        """
        Health check the mongodb instance. Check to see if it has started correctly.
        Method of checking liveness taken from here:
            https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/mongo_ping_client.py
        This was found on this SO thread:
            https://stackoverflow.com/a/53640204
        :param kwargs:
        :return:
        """
        # Message we can send that does not effect the database
        try:
            with socket.create_connection((cls.host_name, 27017)) as connection:
                connection.sendall(PAYLOAD)

                header = connection.recv(16)

                if not header:
                    return False

                # Read the rest of the message
                length = c_int.from_buffer_copy(header[:4]).value
                connection.recv(length - 16)
        except (ConnectionError, ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError):
            return False

        return True
