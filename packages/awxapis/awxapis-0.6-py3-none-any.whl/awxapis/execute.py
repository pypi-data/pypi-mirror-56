import json

from . import config


BASE_URL = config.BASE_URL

def ExecuteTemplate(id, templates, extra_vars=None):
    for template in templates:
        print("Template id: ", template["id"], ", id: ", str(id))
        if str(template["id"]) == str(id):
            response = config.session.get(f"{BASE_URL}{template['related']['launch']}")
            print("Response: ", response.status_code)
            if response.status_code == 200:
                print(response.json())
                data = response.json()
                print("can_start_without_user_input: ", data["can_start_without_user_input"], ", ask_variables_on_launch: ", data["ask_variables_on_launch"])
                if data["can_start_without_user_input"] and not data["ask_variables_on_launch"]:
                    response = config.session.post(f"{BASE_URL}{template['related']['launch']}")
                    print(response.status_code)
                    if response.status_code == 201:
                        data = response.json()
                        print(json.dumps(data, indent=4, sort_keys=True))
                        return template
                elif not data["can_start_without_user_input"] and extra_vars != None:
                    data = {
                        "extra_vars": json.dumps(extra_vars)
                    }
                    response = config.session.post(f"{BASE_URL}{template['related']['launch']}", json=data)
                    print("Status Code: ", response.status_code)
                    data = response.json()
                    print(json.dumps(data, indent=4, sort_keys=True))
                    # if response.status_code == 201:
                    # data = response.json()
                    print(json.dumps(data, indent=4, sort_keys=True))
                    return template

    return None
