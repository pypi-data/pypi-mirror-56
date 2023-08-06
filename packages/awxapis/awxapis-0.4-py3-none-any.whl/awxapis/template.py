import json

from . import config


BASE_URL = config.BASE_URL

def GetJobTemplates():
    response = config.session.get(f"{BASE_URL}/api/v2/job_templates/")

    templates = list()

    print(response.status_code)
    if response.status_code == 200:
        # TODO: try catch block
        data = response.json()["results"]
        for template in data:
            # print(json.dumps(inventory, indent=4, sort_keys=True))
            [id, name] = [template["id"], template["name"]]
            templates.append(template)
            print(f"Name: {name}, id: {id}")

    return templates
