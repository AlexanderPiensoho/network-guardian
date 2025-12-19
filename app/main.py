import requests
import yaml 
from services import ping, req

def main():
    with open ("targets.yml", "r") as file:
        targets = yaml.safe_load(file)

    for target in targets["targets"]:
        name = target["name"]
        target_type = target["type"]

        print(f"kontroll: {name}")

        if target_type == "http":
            status = req(target["url"])
            print(f"status: {status}")
        elif target_type == "ping":
            ping_host = ping(target["host"])
            print(f"Ping: {ping_host}")

if __name__ == "__main__":
    main()
