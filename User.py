class User():
    def __init__(self,api_ip,api_hash):
        self.API_ID = api_ip
        self.API_HASH = api_hash
        self.client = None
    def getAPI_Hash(self):
        return self.API_HASH
    def getAPI_ID(self):
        return self.API_ID
    def getClient(self):
        return self.client
    def setClient(self,client):
        self.client = client