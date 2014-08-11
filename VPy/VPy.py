import slumber
import configController 
import json


class Client():
    settings = configController.configClient("test") ##Default
    api = slumber.API("https://api.validic.com/v1/",  append_slash = False)
    orgId = settings.getOrgId() ##Default
    token = settings.getAccessToken() ##Default
    user = settings.getUser() ##Default

    def init(self, mode):
        self.settings = configController.configClient(mode)
        orgId = self.settings.getOrgId()
        token = self.settings.getAccessToken()
        user = self.settings.getUser()
        return self.settings

    def getMyOrganizationInfo(self):
        response = self.api.organizations(self.orgId).get(access_token = self.token)
        return response

    def getOrganizationInfo(self,orgId):
        response = self.api.organizations(orgId).get(access_token = self.token)
        return response

    def getMyUsers(self):
        response = self.api.organizations(self.orgId).users.get(access_token = self.token)
        return response

    def getUser(self,userId):
        response = self.api.organizations(self.orgId).users(userId).get(access_token = self.token)
        return response

    def refreshUserAccessToken(self,studentId):
        response = self.api.organizations(self.orgId).users(studentId).refresh_token.get(access_token = self.token)
        return response["user"]

    def getUserProfile(self,token):
        response = self.api.profile.get(authentication_token = token)
        return response["profile"]
    
    def suspendUser(self,userid):        
        response = self.api.organizations(self.orgId).users(userid).put({ "suspend": "1", "access_token": self.token })
        return response

    def addUser(self, userid):      
        payload = {  "user": {    "uid": userid  },"access_token": self.settings.getAccessToken()}
        cleanLoad = json.dumps(payload)
        response = self.api.organizations(self.settings.getOrgId()).users.post(cleanLoad.replace("'",""))
        return response

    def getUserStorefrontUrl(self,token):
        return slumber.url_join("https://app.validic.com/",self.orgId,token)

    def getFitness(self, userid):
        response = self.api.organizations(self.orgId).users(userid).fitness.get(access_token = self.token)
        return response

    def getRoutine(self, userid):
        response = self.api.organizations(self.orgId).users(userid).routine.get(access_token = self.token)
        return response

    def getNutrition(self, userid):
        response = self.api.organizations(self.orgId).users(userid).nutrition.get(access_token = self.token)
        return response

    def getSleep(self, userid):
        response = self.api.organizations(self.orgId).users(userid).sleep.get(access_token = self.token)
        return response

    def getWeight(self, userid):
        response = self.api.organizations(self.orgId).users(userid).weight.get(access_token = self.token)
        return response
     
    def getDiabetesMeasurements(self,userid):
        response = self.api.organizations(self.orgId).users(userid).diabetes.get(access_token = self.token)
        return response
     
    def getBiometricMeasurements(self,userid):
        response = self.api.organizations(self.orgId).users(userid).biometrics.get(access_token = self.token)
        return response
     
    def getTobaccoCessation(self,userid):
        response = self.api.organizations(self.orgId).users(userid).tobacco_cessation.get(access_token = self.token)
        return response 

    def unSuspendUser(self,studentId):        
        response = self.api.organizations(self.orgId).users(studentId).put({ "suspend": "0", "access_token": self.token })
        return response

        
    

