import asyncio
import re


async def ping(dnsName):
    # This is the asynchronous command that it will wait for
    ping_async = await asyncio.create_subprocess_exec('ping', f'{dnsName}', '-c 1', '-w 2', '-4', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await ping_async.communicate()
    if stdout:
        ping_result = stdout.decode()
    if stderr:
        ping_result = stderr.decode()
    ping_result_returncode = int(ping_async.returncode)
    if ping_result_returncode == 0:
        ping_result_ip = (re.search(r'\d+\.\d+\.\d+\.\d+', str(ping_result))).group(0)
        subnet_ip = (re.search(r'\d+\.\d+\.\d+', str(ping_result))).group(0)
        try:
            ping_result_time = str((re.search(r'time=\d+\.\d+', str(ping_result))).group(0)).replace("time=","")
        except:
            ping_result_time = str("0.0")
    else:
        location = 'unknown'
        ping_result_ip = 0
        ping_result_time = 0.0
    return ping_result_returncode, ping_result_ip, ping_result_time, subnet_ip
