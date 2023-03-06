import subprocess

verzia_raw = subprocess.run(['sudo', 'apt', 'update'], stdout=subprocess.PIPE)