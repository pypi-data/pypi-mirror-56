import json

from . import config


BASE_URL = config.BASE_URL

def GetInventories():
    response = config.session.get(f"{BASE_URL}/api/v2/inventories/")

    inventories = list()

    print(response.status_code)
    if response.status_code == 200:
        # TODO: try catch block
        data = response.json()["results"]
        for inventory in data:
            # print(json.dumps(inventory, indent=4, sort_keys=True))
            [id, name] = [inventory["id"], inventory["name"]]
            inventories.append(inventory)
            # print(f"Name: {name}, id: {id}")
    
    return inventories