import argparse
import subprocess


class SshpassUtility:
    def __init__(self, host, password, file_path, protocol='ssh'):
        self.protocol = protocol
        self.host = host
        self.password = password
        self.file_path = file_path
        self.sshpass_command = self.do_command()

    def do_command(self):
        password_access = '-f' if self.file_path else '-p'
        command = ['sshpass', password_access, self.password,
                   self.protocol, self.host]
        return command

    def connect_sshpass(self, *args):
        com = self.sshpass_command
        for el in args:
            com += el
        print('----MY COMMAND----')
        print(*com)
        res = subprocess.Popen(com, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        data, err = res.communicate()
        if res.returncode == 0 and len(err) == 0:
            print('---Command success---')
            print()
            print(data.decode())
        else:
            print(f'Something wrong. ReturnCode = {res.returncode}. Error: {err}')
        return data, err, res.returncode

    def send_alone_sshpass_command(self, *args):
        com = self.sshpass_command + list(args)
        proc = subprocess.Popen(com)
        print('Server listening...')


class SCPUtility(SshpassUtility):
    def __init__(self, host, password, file_path, protocol='scp'):
        super().__init__(host, password, file_path)
        self.protocol = protocol
        self.sshpass_command = self.do_command()

    def do_command(self):
        command = super().do_command()
        return command[:-1]

    def connect_sshpass(self, *args):
        """В Аргументах приходит два пути для копирования"""
        adresses = list(*args)
        com = self.sshpass_command
        com.extend([adresses[0], f'{self.host}:{adresses[1]}'])
        print('---My SCP command---')
        print(*com)
        res = subprocess.Popen(com, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        data, err = res.communicate()
        if res.returncode == 0 and len(err) == 0:
            print('Copying successful')
        else:
            print(f'Something wrong. ReturnCode = {res.returncode}.'
                  f' Error: {err}')


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser('Utility for work with SSH')
        self.parser.add_argument('-p', '--password', dest='password',
                                 help='Password for SSH')
        self.parser.add_argument('-fp', '--file_path', dest='file_path',
                                 action='store_true',
                                 help='Way for password')
        self.parser.add_argument('-pr', '--protocol', default='ssh',
                                 dest='protocol',
                                 help='Protocol ssh or scp(Default ssh)')
        self.parser.add_argument('--host', dest='host',
                                 help='Enter user@ip_adress')
        self.parser.add_argument('-t', '--task', dest='task', nargs='*',
                                 help='What to do on server')
        self.parser.add_argument('--option', dest='option', nargs='*',
                                 help='Options for taks')
        self.args = self.parser.parse_args()


if __name__ == '__main__':
    parser = ArgParser()
    args = parser.args
    args_for_utility = [args.host, args.password, args.file_path]

    option = []
    # !!!!!! велосипед!!!!!
    if args.option:  # если есть опции к команде , добавляем к ним флаги
        option = ['-' + el for el in args.option]  # а что если надо --?

    if args.protocol == 'scp':
        args_for_utility += [args.protocol]
        sshhpass = SCPUtility(*args_for_utility)
        sshhpass.connect_sshpass(args.task)
    else:
        sshpass = SshpassUtility(*args_for_utility)
        sshpass.connect_sshpass(args.task + option)

# sshpass -p superpassword ssh root@superserver.com -p2222 supercommand
# python3 sshpass_interface.py -p 111111 --host mcg@192.168.100.79 -t ./first_task.py /home/mcg/work/ --protocol scp
# python3 sshpass_interface.py -p 111111 --host mcg@192.168.100.79 -t ls
