import subprocess


discovery = subprocess.Popen(['python3', 'discovery.py', f'{device_id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

discovery.wait()

website = subprocess.Popen(['python3', 'web/web.py', f'{device_id}'], shell=True)
