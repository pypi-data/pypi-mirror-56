import json
from bs4 import BeautifulSoup

from . import config


BASE_URL = config.BASE_URL

def GetJobs():
    response = config.session.get(f"{BASE_URL}/api/v2/jobs/")

    jobs = list()

    print(response.status_code)
    if response.status_code == 200:
        # TODO: try catch block
        data = response.json()["results"]
        for job in data:
            # print(json.dumps(job, indent=4, sort_keys=True))
            [id, name] = [job["id"], job["name"]]
            jobs.append(job)
            print(f"Job name: {name}, id: {id}")

    return jobs

def BeautyPrint(html):
    print("\n"*10)
    soup = BeautifulSoup(html, 'html.parser')
    tasks = soup.find_all("div", class_="nocode ansi_fore ansi_back")
    # print(soup.prettify())
    print("PLAY" + tasks[0].get_text().split("PLAY")[1])

def GetJobOutput(id, jobs):
    for job in jobs:
        print("Job id: ", job["id"], ", id: ", id)
        if job["id"] == id:
            response = config.session.get(f"{BASE_URL}{job['related']['stdout']}")
            # print("Response status: ", response.status_code)
            if response.status_code == 200:
                content = response.content
                # print("Content: ", content.decode("utf-8"))
                BeautyPrint(content)
                return content

    return None

def PrintImportantJobFields(job):
    important_fields = ["name", "status", "playbook_counts", "failed", "host_status_counts", "skip_tags"]
    for field in important_fields:
        if field in job:
            print(f"{field}: ", json.dumps(job[field], indent=4, sort_keys=True))

def GetJob(id):
    response = config.session.get(f"{BASE_URL}/api/v2/jobs/{str(id)}/")
    # print("Response status: ", response.status_code)
    if response.status_code == 200:
        job = response.json()
        # print(json.dumps(job, indent=4, sort_keys=True))
    
    return job
