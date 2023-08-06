import Job, Execute, Template, Login, Project, Inventory

def AutoExecute():
    pass

def main():
    # TODO: change the way username and password are taken as input
    token = Login.GetToken()
    print("Token: ", token)
    if not token:
        return
    
    # inventories = Inventory.GetInventories(session, )
    # del inventories
    # templates = Template.GetJobTemplates(session, )

    # execute_template_id = int(input("Enter template id to execute: "))
    # Execute.ExecuteTemplate(session, execute_template_id, templates)

    jobs = Job.GetJobs()
    job_id = int(input("Enter job id to show output of: "))
    Job.GetJobOutput(job_id, jobs)
    job = Job.GetJob(job_id)
    print("\n"*10 + "Important Job Fields: ")
    Job.PrintImportantJobFields(job)

if __name__ == "__main__":
    main()
