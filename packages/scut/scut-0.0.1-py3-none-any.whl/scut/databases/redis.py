from docker.models.containers import Container

from bunt.containers import ContainerConfiguration
from bunt.containers import ContainerConfigurationClientConnectable
from bunt.containers import ContainerConfigurationHealthCheck

try:
    from redis import Redis
except:
    Redis = None


class RedisContainer(
    ContainerConfiguration,
    ContainerConfigurationHealthCheck,
    ContainerConfigurationClientConnectable
):
    """
    Start an ephemeral Redis instance within your testing environment.
    """
    host_name = 'redis'

    image = 'redis:5.0.6-alpine'

    tcp_ports = frozenset({
        6379,
    })

    connectable_container_type = Redis

    @classmethod
    def connection(cls, **kwargs):
        if Redis is None:
            raise RuntimeError('Redis driver is not installed. Please install redis.')
        return Redis.from_url(f'redis://{cls.host_name}:6379')

    @classmethod
    def health_check(cls, *, container: Container, **kwargs) -> bool:
        """
        :param container: Docker container we are trying to start
        :param kwargs:
        :return:
        """
        try:
            result = container.exec_run(cmd=['redis-cli', 'info'])
            return result.exit_code == 0
        except:
            return False
