import os
import json
import requests
import logging

# Get ENV variables.
def getENV():
  githubJson = os.environ['GITHUB_JSON']
  githubToken = os.environ['GITHUB_TOKEN']
  github = json.loads(githubJson)
  jiraUser = os.environ['JIRA_USER']
  jiraPass = os.environ['JIRA_TOKEN']

  return github, githubToken, jiraUser, jiraPass

def createJiraTicket(jiraUser, jiraPass, githubPRTitle, githubPRURL):
  jiraUrl = os.environ.get('JIRA_URL')
  jiraHeaders = {"Content-Type": "application/json"}
  jiraBody = {
    "fields": {
      "project": {"key": os.environ.get('JIRA_PROJECT')},
      "summary": "[Dependabot]: " + f"{githubPRTitle}",
      "description": f"{githubPRURL} | {jiraUser}",
      "issuetype": {"name": "Tiket"}
    }
  }
  response = requests.post(jiraUrl, auth=(jiraUser, jiraPass), headers=jiraHeaders, json=jiraBody)
  logging.debug(response.text)
  print(response.status_code)
  if response.status_code == 201:
    jiraResponse = json.loads(response.text)
    return jiraResponse['key']

# Make API call to GitHub to change PR title.
def updateGithubPRTitle(githubToken, jiraKey, githubPRTitle, githubRepo, githubPRNum):
  githubHeaders = {"Authorization": f"token {githubToken}"}
  githubBody = {"title": f"{jiraKey} | {githubPRTitle}"}
  githubUrl = f"https://api.github.com/repos/{githubRepo}/pulls/{githubPRNum}"
  response = requests.patch(githubUrl, json=githubBody, headers=githubHeaders)
  print(response.status_code)

if __name__ == "__main__":
  github, githubToken, jiraUser, jiraPass = getENV()

  githubRepo = github['repository']
  githubPRURL = github['event']['pull_request']['_links']['html']['href']
  githubPRTitle = github['event']['pull_request']['title']
  githubPRNum = github['event']['pull_request']['number']

  jiraKey = createJiraTicket(jiraUser, jiraPass, githubPRTitle, githubPRURL)
  print(jiraKey)
  updateGithubPRTitle(githubToken, jiraKey, githubPRTitle, githubRepo, githubPRNum)