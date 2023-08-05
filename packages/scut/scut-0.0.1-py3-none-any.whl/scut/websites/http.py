from bunt.containers import ContainerConfigurationHttp
from bunt.containers import ContainerConfigurationHttpHealthCheck


class TutumHelloWorldContainer(
    ContainerConfigurationHttp,
    ContainerConfigurationHttpHealthCheck
):
    name = 'tatum_hello_world'
    image = 'tutum/hello-world:latest'
    host_name = 'tatum_hello_world'

    http_protocol = 'http'
    http_port = 80

    http_health_check_path = '/'
