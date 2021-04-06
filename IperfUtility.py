import argparse
import subprocess

from parser_iperf_results import parser_iperf_results as pir
from sshpass_interface import SshpassUtility, ArgParser


class NetworkUtility(SshpassUtility):
    def __init__(self, host, password, protocol='ssh', host_2=None):
        super().__init__(host, password)
        self.host_2 = host_2
        self.sshpass_command = super().do_command(self.password)


class IperfParser(ArgParser):
    def __init__(self):  # почему не могу отнаследоваться от родителя и добавить свои элементы?
        self.parser = argparse.ArgumentParser('IPERf parser')
        self.parser.add_argument('-p', '--password', dest='password',
                                 help='Password for SSH host_1')
        self.parser.add_argument('-p_2', '--password_2', dest='password_2',
                                 help='Password for SSH host_2')
        self.parser.add_argument('-fp', '--file_path', dest='file_path',
                                 help='Way for password')
        self.parser.add_argument('--host', help='Servers IP Adress')
        self.parser.add_argument('--host_2', help='Clinets IP Adress')
        self.parser.add_argument('--start', dest='start_test', nargs='?',
                                 const='-c', help='flag for client')
        self.parser.add_argument('--open', nargs='?', const='-1',
                                 help='open connection for one request')
        self.parser.add_argument('-t', dest='task', default='iperf3',
                                 help='Main command')
        self.args = self.parser.parse_args()


if __name__ == '__main__':
    parser = IperfParser()
    args = parser.args
    args_for_utility = [args.host, args.password]
    sshpass_server = NetworkUtility(*args_for_utility)
    sshpass_client = SshpassUtility(args.host_2, args.password_2)

    if args.open:
        sshpass_server.send_alone_sshpass_command(args.task, '-s', args.open)
    if args.start_test:
        sshpass_server.connect_sshpass([*sshpass_client.sshpass_command,
                                        args.task, '-c', args.host[4:]]) # временное решение под мой сервер
