from requests import request
import yaml 


with open ("targets.yml", "r") as file:
    targets = yaml.safe_load(file)

print(targets)
