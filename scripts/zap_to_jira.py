# Post a new issue to JIRA
import os
import logging
import requests 
from datetime import datetime

# Write the report into a file
filename = 'report_html.html'
base_url = os.environ.get('JIRA_BASE_URL')
str_date = datetime.now().strftime('%Y-%m-%d %H:%M')
descr = "ZAP security test produced the following HTML report."
details = ""
details.replace("\t", "    ")
new_issue_data = {
    "fields": {
        "project": { "key": os.environ.get('JIRA_PROJECT') },
        "summary": "[ZAP Security Report] - " + str_date,
        "description": details + "\n\n" + descr,
        "issuetype": { "name": "Bug" },
        "priority": { "id": "2" },
        "assignee": { "name": "" }
    }
}
logging.debug(new_issue_data)
auth = (os.environ.get('JIRA_USER'), os.environ.get('JIRA_TOKEN'))
r = requests.post(base_url, json=new_issue_data, auth=auth)
logging.debug(r.text)
response_in_json = r.json()
issue_key = response_in_json["id"]
# Add the html report as an attachment
r = requests.post(base_url + "/{}/attachments".format(issue_key), auth=auth,
    headers={"X-Atlassian-Token": "no-check"},
    files={'file': ('report_html.html', open(filename, 'rb'),  "text/html")})
logging.debug(r.text)
# if( not critical ): # mark closed
#     r = requests.post(base_url + "/{}/transitions".format(issue_key), auth=auth,
#         json={ "transition": { "id": "2" } })
logging.debug("Report complete")