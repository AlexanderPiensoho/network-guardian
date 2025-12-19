import requests

def req(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code
    except:
        return "Connection error"

def ping():
    print("ping")
