import json
from bs4 import BeautifulSoup

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
            print(f"Template name: {name}, id: {id}")

    return templates

def GetJobs(template_id):
    response = config.session.get(f"{BASE_URL}/api/v2/job_templates/{str(template_id)}/jobs/")

    jobs = None

    print(response.status_code)
    if response.status_code == 200:
        # TODO: try catch block
        jobs = response.json()["results"]
        for job in jobs:
            # print(json.dumps(inventory, indent=4, sort_keys=True))
            [id, name] = [job["id"], job["name"]]
            print(f"Job name: {name}, id: {id}")

    return jobs

def GetLastJob(template_id):
    response = config.session.get(f"{BASE_URL}/api/v2/job_templates/{str(template_id)}/")

    print(response.status_code)
    if response.status_code == 200:
        # TODO: try catch block

        data = response.json()
        if "last_job" in data["related"]:
            return data["related"]["last_job"].split("/")[-2], data["related"]["last_job"]

    return None

def BeautyPrint(html):
    print("\n"*10)
    soup = BeautifulSoup(html, 'html.parser')
    tasks = soup.find_all("div", class_="nocode ansi_fore ansi_back")
    # print(soup.prettify())
    print(tasks)
    print("PLAY" + tasks[0].get_text().split("PLAY")[1])

def GetJobOutput(job_id):
    response = config.session.get(f"{BASE_URL}/api/v2/jobs/{job_id}/stdout/?format=txt_download")

    print(response.status_code)
    if response.status_code == 200:
        # TODO: try catch block
        # BeautyPrint(content)
        return response.content.decode("utf-8")

    return None
