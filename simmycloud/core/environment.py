
from core.server import Server

class Environment:

    def __init__(self, environment_builder):
        self._builder = environment_builder
        self._online_servers = {}
        self._offline_servers = {}
        self._vm_hosts = {}
        self._logger = None
        self._config = None

    def set_config(self, config):
        self._config = config

    def initialize(self):
        self._logger = self._config.getLogger(self)
        self._builder.build(self)

    def add_servers_of_type(self, server, quantity=1):
        servers_count = len(self._online_servers) + len(self._offline_servers) + 1
        while quantity > 0:
            self._offline_servers[str(servers_count)] = Server(str(servers_count),
                                                               server.cpu,
                                                               server.mem
                                                               )
            quantity -= 1
            servers_count += 1

    def turn_on_server(self, server_name):
        self._config.statistics.add_to_counter('servers_turned_on')
        self._logger.debug('Server {} being turned on'.format(server_name))
        server = self._offline_servers.pop(server_name)
        self._online_servers[server_name] = server
        return server

    def turn_off_server(self, server_name):
        self._config.statistics.add_to_counter('servers_turned_off')
        self._logger.debug('Server {} being turned off'.format(server_name))
        server = self._online_servers.pop(server_name)
        self._offline_servers[server_name] = server

    def schedule_vm_at_server(self, vm, server_name):
        self._logger.debug('Allocating VM {} to server {}'.format(vm.name, server_name))
        self._online_servers[server_name].schedule_vm(vm)
        self._vm_hosts[vm.name] = server_name

    def get_server_of_vm(self, vm_name):
        server_name = self._vm_hosts[vm_name]
        return self._online_servers[server_name]

    def online_servers(self):
        return self._online_servers.values()

    def offline_servers(self):
        return self._offline_servers.values()

    def all_servers(self):
        return self._online_servers.values() + self._online_servers.values()


class EnvironmentBuilder:

    @staticmethod
    def build():
        raise NotImplementedError
