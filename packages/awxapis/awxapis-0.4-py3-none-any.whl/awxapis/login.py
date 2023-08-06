import base64, json, getpass

from . import config


BASE_URL = config.BASE_URL

def GetToken(**kwargs):
    if "username" not in kwargs or "password" not in kwargs:
        return None
    username = str(kwargs["username"])
    password = str(kwargs["password"])
    authorization_header = base64.b64encode(f"{username}:{password}".encode("utf-8"))
    headers = {
        "Authorization": f"Basic {authorization_header.decode('utf-8')}",
        "Content-Type": "application/json"
    }
    response = config.session.post(f"{BASE_URL}/api/v2/tokens/", headers=headers, data={})
    data = json.loads(response.content.decode("utf-8"))

    if "token" not in data:
        return None

    config.session.headers.update({"Authorization": f"Bearer {data['token']}"})
    config.session.headers.update({"Content-Type": "application/json"})

    return data["token"]
