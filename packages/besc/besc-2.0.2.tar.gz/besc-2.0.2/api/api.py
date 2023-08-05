import requests
import json

async def getLastData(client, keyPair):

    client.setprojectid(keyPair.projectId)
    client.setendpoint("/debugs/:project_id")
    extraPath = "/last"
    response = requests.get(client.buildUrl()+extraPath,
                            headers={
                                "apikey": keyPair.apiKey,
                                "Content-Type": "application/json"
                            })

    json_response = response.json()

    return json_response


async def getProjectData(client, keyPair, queryOptions):
    client.setprojectid(keyPair.projectId)
    client.setendpoint("/project/:project_id")

    try:
        response = requests.get(client.buildUrl(),
                            headers={
                                "apikey": keyPair.apiKey,
                                "Content-Type": "application/json"
                            })

        json_response = response.json()

    except AttributeError as err:
        json_response = err

    return json_response


async def sendProjectData(client, keyPair, projectdata):
    client.setprojectid(keyPair.projectId)
    client.setendpoint("/project/:project_id")
    serializedData = projectdata.serialize()
    json_str = json.dumps(serializedData)

    data = json.loads(json_str)

    response = requests.post(client.buildUrl(),
                             data=data['data'],
                             headers={
                                 "apikey": keyPair.apiKey,
                                 "Content-Type": "application/json",
                                 "checksum": data['checksum']
                             })

    json_response = response.json()

    return json_response