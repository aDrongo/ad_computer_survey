import subprocess
import re


def ping(dnsName):
    result = subprocess.run(['ping', '-4', '-c 1', '-w 5', dnsName], capture_output=True)
    if result.returncode == 0:
        result.ip = (re.search(r'\d+\.\d+\.\d+\.\d+', str(result.stdout))).group(0)
        try:
            result.time = str((re.search(r'time=\d+\.\d+', str(result.stdout))).group(0)).replace("time=","")
        except:
            result.time = str("0.0")
    else:
        result.ip = 0
        result.time = 0.0
    return result
