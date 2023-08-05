class besc_ess_host:

    def __init__(self, host):
        self.host = host


    def createDefault(self):
        return besc_ess_host("http://carboapi.besc.online/besc-data")

    def setendpoint(self, endpoint):
        self.endpoint = endpoint

    def setprojectid(self, projectid):
        self.projectid = projectid

    def buildUrl(self):
        endpoint = self.endpoint.replace(":project_id", self.projectid)

        return self.host + basePath + endpoint


endpoints = {
    "debug": "/debugs/:project_id",
    "project": "/project/:project_id"
}

basePath = "/energysaving"
