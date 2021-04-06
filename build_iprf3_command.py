def build_command(*args):
    if args.open:
        return['iperf3', '-s', '-1']
    if args.start_test:
        iperf_command = ['iperf3', '-c', args.host]
        sshpass_command = ['sshpass', '-p', args.password, 'ssh', args.host_2]
        return sshpass_command, iperf_command
