import os
import sys
import json
import base64
import requests

from domain import FlowName, JobBuildNumber, AgentToken, Job, ServerUrl, AgentJobDir

HttpHeaders = {
    "AGENT-TOKEN": AgentToken
}

def GetVar(name, required=True):
    val = os.environ.get(name)
    if required and val is None:
        sys.exit("{} is missing".format(name))
    return val


def GetCurrentJob():
    return Job()


def ToBase64String(strVal):
    b64bytes = base64.b64encode(strVal.encode("utf-8"))
    return str(b64bytes, 'utf-8')


def FindFiles(file, path = AgentJobDir):
    files = []

    for i in os.listdir(path):
        fullPath = os.path.join(path, i)

        if os.path.isdir(fullPath) and not i.startswith("."):
            files += FindFiles(file, fullPath)

        if os.path.isfile(fullPath) and i == file:
            files.append(fullPath)

    return files


class Client:
    def __init__(self):
        pass

    def getCredential(self, name):
        try:
            url = "{}/api/credential/{}".format(ServerUrl, name)
            r = requests.get(url=url, headers=HttpHeaders)
            if r.status_code is 200:
                body = r.text
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None

    def listFlowUsers(self):
        try:
            url = "{}/api/flow/{}/users".format(ServerUrl, FlowName)
            r = requests.get(url=url, headers=HttpHeaders)

            if r.status_code is 200:
                body = r.text
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None

    def sendJobReport(self, path, body):
        try:
            url = "{}/api/flow/{}/job/{}/report".format(
                ServerUrl, FlowName, JobBuildNumber)
            r = requests.post(url=url, headers=HttpHeaders, files={
                'file': open(path, 'rb'),
                'body': ('', json.dumps(body), 'application/json')
            })
            return r.status_code
        except Exception as e:
            print(e)
            return -1

    def sendStatistic(self, body):
        try:
            url = "{}/api/flow/{}/stats".format(ServerUrl, FlowName)
            r = requests.post(url=url, headers=HttpHeaders, data=json.dumps(body))
            return r.status_code
        except Exception as e:
            print(e)
            return -1

    def addJobContext(self, var):
        try:
            url = "{}/api/flow/{}/job/{}/context".format(ServerUrl, FlowName, JobBuildNumber)
            r = requests.post(url=url, headers=HttpHeaders,
                              data=json.dumps(var))
            return r.status_code
        except Exception as e:
            print(e)
            return -1