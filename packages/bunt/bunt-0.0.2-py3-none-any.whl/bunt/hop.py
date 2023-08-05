from bunt.containers import ContainerConfiguration


class BuntContainer(ContainerConfiguration):
    name = 'bunt'
    host_name = 'bunt'

    image = 'bunt/bunt:latest'

    entry_point = ['bunt']
    command = []

    volume_mounts = {
        '/var/run/docker.sock': '/var/run/docker.sock'
    }
