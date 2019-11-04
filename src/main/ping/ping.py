import subprocess
import sys

def ping(device):
    ping = subprocess.run(['ping', f'{device}', '-c 1', '-w 2', '-4'], capture_output=True)
    print(ping.returncode)
    if int(ping.returncode) != 0:
        print('trying ping')
        ping = subprocess.run(['ping', f'{device}', '-c 1', '-w 2', '-6'], capture_output=True)
        print(ping)
    return ping

ping(sys.argv[1])
