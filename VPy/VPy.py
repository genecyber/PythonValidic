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
            try:
                self.deleteUser(user["_id"].encode('utf-8'))
            except Exception: 
                continue #Probably trying to delete a user that cannot be deleted so lets skip
        

    def deleteUser(self, userId):
        try:    
            self.api.organizations(self.orgId).users(userId).delete(access_token = self.token)
        except Exception:
            pass
        response = userId;

    def addUser(self, userid):      
        payload = {  "user": { "uid": userid  },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users.post(payload)
        return response

    def addUserWithProfile(self, userid, profile):      
        payload = {  "user": { "uid": userid, "profile":{ "gender": profile.gender, "location": profile.location, "birth_year": profile.birthyear, "height": profile.height, "weight": profile.weight } },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users.post(payload)
        return response

    def addFitness(self, userId, fitness):
        payload = { "fitness":{ "timestamp": fitness.timestamp,"utc_offset": fitness.utc_offset, "type": fitness.type, "intensity": fitness.intensity,"start_time": fitness.start_time,"distance": fitness.distance,"duration": fitness.duration,"calories": fitness.calories,"activity_id": fitness.activity_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userId).fitness().post(payload)
        return response

    def addRoutine(self, userid, routine):
        payload = { "routine":{ "timestamp": routine.timestamp, "utc_offset": routine.utc_offset, "steps": routine.steps, "distance": routine.distance, "floors": routine.floors, "elevation": routine.elevation, "calories_burned": routine.calories_burned, "activity_id": routine.activity_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).routine().post(payload)
        return response

    def addNutrition(self, userid, nutrition):
        payload = { "nutrition":{ "timestamp": nutrition.timestamp, "utc_offset": nutrition.utc_offset, "calories": nutrition.calories, "carbohydrates": nutrition.carbohydrates, "fat": nutrition.fat, "fiber": nutrition.fiber, "protein": nutrition.protein, "sodium": nutrition.sodium, "water": nutrition.water, "meal": nutrition.meal, "entry_id": nutrition.entry_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).nutrition().post(payload)
        return response
    
    def addSleep(self, userid, sleep):
        payload = { "sleep":{ "timestamp": sleep.timestamp, "utc_offset": sleep.utc_offset, "total_sleep": sleep.total_sleep, "awake": sleep.awake, "deep": sleep.deep, "light": sleep.light, "rem": sleep.rem, "times_woken": sleep.times_woken, "activity_id": sleep.activity_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).sleep().post(payload)
        return response
    
    def addWeight(self, userid, weight):
        payload = { "weight":{ "timestamp": weight.timestamp, "utc_offset": weight.utc_offset, "weight": weight.weight, "height": weight.height, "free_mass": weight.free_mass, "fat_percent": weight.fat_percent, "mass_weight": weight.mass_weight, "bmi": weight.bmi, "data_id": weight.data_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).weight().post(payload)
        return response
    
    def addDiabetes(self, userid, diabetes):
        payload = { "diabetes":{ "timestamp": diabetes.timestamp, "utc_offset": diabetes.utc_offset, "c_peptide": diabetes.c_peptide, "fasting_plasma_glucose_test": diabetes.fasting_plasma_glucose_test, "hba1c": diabetes.hba1c, "insulin": diabetes.insulin, "oral_glucose_tolerance_test": diabetes.oral_glucose_tolerance_test, "random_plasma_glucose_test": diabetes.random_plasma_glucose_test, "triglyceride": diabetes.triglyceride, "blood_glucose": diabetes.blood_glucose, "activity_id": diabetes.activity_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).diabetes().post(payload)
        return response
    
    def addBiometrics(self, userid, biometrics):
        payload = { "biometrics":{  "timestamp": biometrics.timestamp, "utc_offset": biometrics.utc_offset, "blood_calcium": biometrics.blood_calcium, "blood_chromium": biometrics.blood_chromium, "blood_folic_acid": biometrics.blood_folic_acid, "blood_magnesium": biometrics.blood_magnesium, "blood_potassium": biometrics.blood_potassium, "blood_sodium": biometrics.blood_sodium, "blood_vitamin_b12": biometrics.blood_vitamin_b12, "blood_zinc": biometrics.blood_zinc, "creatine_kinase": biometrics.creatine_kinase, "crp": biometrics.crp, "diastolic": biometrics.diastolic, "ferritin": biometrics.ferritin,"hdl": biometrics.hdl, "hscrp": biometrics.hscrp, "il6": biometrics.il6, "ldl": biometrics.ldl, "resting_heartrate": biometrics.resting_heartrate, "systolic": biometrics.systolic, "testosterone": biometrics.testosterone, "total_cholesterol": biometrics.total_cholesterol, "tsh": biometrics.tsh,"uric_acid": biometrics.uric_acid,"vitamin_d": biometrics.vitamin_d,"white_cell_count": biometrics.white_cell_count,"spo2": biometrics.spo2,"temperature": biometrics.temperature,"data_id": biometrics.data_id },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).biometrics().post(payload)
        return response
    
    def addTobaccoCessation(self, userid, tobacco_cessation):
        payload = { "tobacco_cessation":{ "timestamp": tobacco_cessation.timestamp, "utc_offset": tobacco_cessation.utc_offset, "cigarettes_allowed": tobacco_cessation.cigarettes_allowed, "cigarettes_smoked": tobacco_cessation.cigarettes_smoked, "cravings": tobacco_cessation.cravings, "last_smoked": tobacco_cessation.last_smoked },"access_token": self.settings.getAccessToken()}
        response = self.api.organizations(self.settings.getOrgId()).users(userid).tobacco_cessation().post(payload)
        return response



        
    

