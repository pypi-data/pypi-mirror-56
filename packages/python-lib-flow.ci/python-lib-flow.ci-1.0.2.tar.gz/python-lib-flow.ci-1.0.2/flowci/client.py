import os
import json
import base64
import http.client

from .domain import Job, ServerUrl

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

class Client:
    def __init__(self):
        pass

    def createConn():
        if ServerUrl.startswith("http://"):
            return http.client.HTTPConnection(ServerUrl.lstrip("http://"))

        return http.client.HTTPConnection(ServerUrl.lstrip("https://"))

    def getCredential(name):
        try:
            path = "/api/credential/{}".format(name)
            conn = createConn()
            conn.request(method="GET", url=path, headers=HttpHeaders)

            response = conn.getresponse()
            if response.status is 200:
                body = response.read()
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None

    def listFlowUsers():
        try:
            path = "/api/flow/{}/users".format(FlowName)
            conn = createConn()
            conn.request(method="GET", url=path, headers=HttpHeaders)
            response = conn.getresponse()

            if response.status is 200:
                body = response.read()
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None

    def sendSummary(body):
        try:
            path = "/api/flow/{}/job/{}/summary".format(FlowName, BuildNumber)
            conn = createConn()
            conn.request("POST", path, json.dumps(body), HttpHeaders)
            return conn.getresponse().status
        except Exception as e:
            print(e)
            return -1


    def sendStatistic(body):
        try:
            path = "/api/flow/{}/stats".format(FlowName)
            conn = createConn()
            conn.request("POST", path, json.dumps(body), HttpHeaders)
            return conn.getresponse().status
        except Exception as e:
            print(e)
            return -1