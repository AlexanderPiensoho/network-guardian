import requests
import subprocess

def req(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code
    except:
        return "Connection error"

def ping(host):
    try:
        output = subprocess.check_output(["ping", "-c", "4", host])
        return output.decode()
    except subprocess.CalledProcessError:
        return f"Could not ping {host}"
