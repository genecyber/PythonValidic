import slumber
import configController 
import json


class Client():
    settings = configController.configClient("test") ##Default
    api = slumber.API(settings.getApi(),  append_slash = False)
    orgId = settings.getOrgId() ##Default
    token = settings.getAccessToken() ##Default
    user = settings.getUser() ##Default

    def init(self, mode):
        self.settings = configController.configClient(mode)
        orgId = self.settings.getOrgId()
        token = self.settings.getAccessToken()
        user = self.settings.getUser()
        self.orgId = self.settings.getOrgId()
        self.token = self.settings.getAccessToken()
        self.user = self.settings.getUser()
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

    def unSuspendUser(self,userId):        
        response = self.api.organizations(self.orgId).users(userId).put({ "suspend": "0", "access_token": self.token })
        return response

    def deleteAllUsers(self):
        response = self.getMyUsers()
        for user in response["users"]:
            self.deleteUser(user["_id"].encode('utf-8'))

    def deleteUser(self, userId):
        try:    
            self.api.organizations(self.orgId).users(userId).delete(access_token = self.token)
        except Exception:
            pass
        response = userId;

    def addUser(self, userid):      
        payload = {  "user": {    "uid": userid  },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users.post(payload)
        return response

    def addUserWithProfile(self, userid, gender, location, birthyear, height, weight):      
        payload = {  "user": {    "uid": userid, "profile":{ "gender": gender, "location": location, "birth_year": birthyear, "height": height, "weight": weight } },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users.post(payload)
        return response

    def addFitness(self, userId,timestamp,utc_offset,type,intensity,start_time,distance,duration,calories,activity_id):
        payload = {   "fitness":{ "timestamp": timestamp,"utc_offset": utc_offset,"type": type,"intensity": intensity,"start_time": start_time,"distance":distance,"duration": duration,"calories": calories,"activity_id": activity_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userId).fitness().post(payload)
        return response

    def addRoutine(self, userid, routine):
        return true


        
    

