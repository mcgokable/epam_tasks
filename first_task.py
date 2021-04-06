import argparse
import json
import subprocess


class DiskUtility:
    def __init__(self, command='df'):
        self.command = command

    def do_command(self, arg=None):
        if arg is not None:
            res = subprocess.Popen([self.command, arg],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        else:
            res = subprocess.Popen([self.command],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        data, err = res.communicate()  # ждем завершения
        status = res.returncode
        self.result_to_json(data, err.decode(), status)

    def result_to_json(self, data, err, status):
        result = [el.split() for el in data.decode().splitlines()[1:]]  # что придет если ошибка?
        error = 'None' if err == '' else err.strip()
        status = 'success' if status == 0 else 'failure'
        data_for_json = {'status': status, 'error': error, 'result': result}
        res_json = json.dumps(data_for_json)
        print(res_json)


class ArgParser:
    def __init__(self, description='No description'):
        self.parser = argparse.ArgumentParser(description=description)
        self.parser.add_argument('--human', help='Linux system command df -h',
                                 action='store_true', dest='human')
        self.parser.add_argument('--inode', help='Linux system command df -i',
                                 action='store_true', dest='inode')
        self.args = self.parser.parse_args()


if __name__ == '__main__':
    parser = ArgParser('My first CLI parser')
    args = parser.args
    disk_util = DiskUtility()
    if args.inode or args.human:
        util_args = '-i' if args.inode else '-h'
        disk_util.do_command(util_args)
    else:
        disk_util.do_command()
