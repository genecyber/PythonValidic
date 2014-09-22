import slumber
import configController 
import json
import Filter
from slumber.serialize import BaseSerializer
from slumber import serialize

class FilteredSerializer(BaseSerializer):
    key = "jsonFiltered"
    content_types = [
                        "application/json",
                        "application/x-javascript",
                        "text/javascript",
                        "text/x-javascript",
                        "text/x-json",
                    ]

    def loads(self, data):
        return json.loads(data)

    def dumps(self, data):
        return json.dumps(data)


class Client():
    settings = configController.configClient("test") ##Default
    
    s = serialize.Serializer(
                default="jsonFiltered",
                serializers=[
                    serialize.JsonSerializer(),
                    serialize.YamlSerializer(),
                    FilteredSerializer(),
                ]
            )

    api = slumber.API(settings.getApi(),  append_slash = False, format = "jsonFiltered", serializer=s)
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
        self.filter_dict = {"access_token" : self.token}
        return self.settings

    def Filtered(self, **kwargs):
        kwargs["access_token"] = self.token
        self.filter_dict = kwargs
        return self

    def getMyOrganizationInfo(self):
        response = self.api.organizations(self.orgId).get(**self.filter_dict)
        return response

    def getOrganizationInfo(self,orgId):
        response = self.api.organizations(orgId).get(**self.filter_dict)
        return response

    def getMyUsers(self):
        response = self.api.organizations(self.orgId).users.get(**self.filter_dict)
        return response

    def getUser(self,userId):
        response = self.api.organizations(self.orgId).users(userId).get(**self.filter_dict)
        return response

    def refreshUserAccessToken(self,studentId):
        response = self.api.organizations(self.orgId).users(studentId).refresh_token.get(**self.filter_dict)
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
        response = self.api.organizations(self.orgId).users(userid).fitness.get(**self.filter_dict)
        return response

    def getRoutine(self, userid):
        response = self.api.organizations(self.orgId).users(userid).routine.get(**self.filter_dict)
        return response

    def getNutrition(self, userid):
        response = self.api.organizations(self.orgId).users(userid).nutrition.get(**self.filter_dict)
        return response

    def getSleep(self, userid):
        response = self.api.organizations(self.orgId).users(userid).sleep.get(**self.filter_dict)
        return response

    def getWeight(self, userid):
        response = self.api.organizations(self.orgId).users(userid).weight.get(**self.filter_dict)
        return response
     
    def getDiabetesMeasurements(self,userid):
        response = self.api.organizations(self.orgId).users(userid).diabetes.get(**self.filter_dict)
        return response
     
    def getBiometricMeasurements(self,userid):
        response = self.api.organizations(self.orgId).users(userid).biometrics.get(**self.filter_dict)
        return response
     
    def getTobaccoCessation(self,userid):
        response = self.api.organizations(self.orgId).users(userid).tobacco_cessation.get(**self.filter_dict)
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
        payload = self.populateFitness(fitness)
        response = self.api.organizations(self.settings.getOrgId()).users(userId).fitness().post(payload)
        return response
    
    def populateFitness(self, fitness):
        return { "fitness":{ "timestamp": fitness.timestamp,"utc_offset": fitness.utc_offset, "type": fitness.type, "intensity": fitness.intensity,"start_time": fitness.start_time,"distance": fitness.distance,"duration": fitness.duration,"calories": fitness.calories,"activity_id": fitness.activity_id },"access_token": self.settings.getAccessToken()}

    def addRoutine(self, userid, routine):
        payload = self.populateRoutine(routine)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).routine().post(payload)
        return response

    def populateRoutine(self, routine):
        return { "routine":{ "timestamp": routine.timestamp, "utc_offset": routine.utc_offset, "steps": routine.steps, "distance": routine.distance, "floors": routine.floors, "elevation": routine.elevation, "calories_burned": routine.calories_burned, "activity_id": routine.activity_id },"access_token": self.settings.getAccessToken()}
    
    def addNutrition(self, userid, nutrition):
        payload = self.populateNutrition(nutrition)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).nutrition().post(payload)
        return response

    def populateNutrition(self, nutrition):
        return { "nutrition":{ "timestamp": nutrition.timestamp, "utc_offset": nutrition.utc_offset, "calories": nutrition.calories, "carbohydrates": nutrition.carbohydrates, "fat": nutrition.fat, "fiber": nutrition.fiber, "protein": nutrition.protein, "sodium": nutrition.sodium, "water": nutrition.water, "meal": nutrition.meal, "entry_id": nutrition.entry_id },"access_token": self.settings.getAccessToken()}

    def addSleep(self, userid, sleep):
        payload = self.populateSleep(sleep)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).sleep().post(payload)
        return response

    def populateSleep(self, sleep):
        return { "sleep":{ "timestamp": sleep.timestamp, "utc_offset": sleep.utc_offset, "total_sleep": sleep.total_sleep, "awake": sleep.awake, "deep": sleep.deep, "light": sleep.light, "rem": sleep.rem, "times_woken": sleep.times_woken, "activity_id": sleep.activity_id },"access_token": self.settings.getAccessToken()}
        
    def addWeight(self, userid, weight):
        payload = self.populateWeight(weight)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).weight().post(payload)
        return response

    def populateWeight(self, weight):
        return { "weight":{ "timestamp": weight.timestamp, "utc_offset": weight.utc_offset, "weight": weight.weight, "height": weight.height, "free_mass": weight.free_mass, "fat_percent": weight.fat_percent, "mass_weight": weight.mass_weight, "bmi": weight.bmi, "data_id": weight.data_id },"access_token": self.settings.getAccessToken()}
        
    def addDiabetes(self, userid, diabetes):
        payload = self.populateDiabetes(diabetes)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).diabetes().post(payload)
        return response

    def populateDiabetes(self, diabetes):
        return { "diabetes":{ "timestamp": diabetes.timestamp, "utc_offset": diabetes.utc_offset, "c_peptide": diabetes.c_peptide, "fasting_plasma_glucose_test": diabetes.fasting_plasma_glucose_test, "hba1c": diabetes.hba1c, "insulin": diabetes.insulin, "oral_glucose_tolerance_test": diabetes.oral_glucose_tolerance_test, "random_plasma_glucose_test": diabetes.random_plasma_glucose_test, "triglyceride": diabetes.triglyceride, "blood_glucose": diabetes.blood_glucose, "activity_id": diabetes.activity_id },"access_token": self.settings.getAccessToken()}
        
    def addBiometrics(self, userid, biometrics):
        payload = self.populateBiometrics(biometrics)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).biometrics().post(payload)
        return response

    def populateBiometrics(self, biometrics):
        return { "biometrics":{  "timestamp": biometrics.timestamp, "utc_offset": biometrics.utc_offset, "blood_calcium": biometrics.blood_calcium, "blood_chromium": biometrics.blood_chromium, "blood_folic_acid": biometrics.blood_folic_acid, "blood_magnesium": biometrics.blood_magnesium, "blood_potassium": biometrics.blood_potassium, "blood_sodium": biometrics.blood_sodium, "blood_vitamin_b12": biometrics.blood_vitamin_b12, "blood_zinc": biometrics.blood_zinc, "creatine_kinase": biometrics.creatine_kinase, "crp": biometrics.crp, "diastolic": biometrics.diastolic, "ferritin": biometrics.ferritin,"hdl": biometrics.hdl, "hscrp": biometrics.hscrp, "il6": biometrics.il6, "ldl": biometrics.ldl, "resting_heartrate": biometrics.resting_heartrate, "systolic": biometrics.systolic, "testosterone": biometrics.testosterone, "total_cholesterol": biometrics.total_cholesterol, "tsh": biometrics.tsh,"uric_acid": biometrics.uric_acid,"vitamin_d": biometrics.vitamin_d,"white_cell_count": biometrics.white_cell_count,"spo2": biometrics.spo2,"temperature": biometrics.temperature,"data_id": biometrics.data_id },"access_token": self.settings.getAccessToken()}
        
    def addTobaccoCessation(self, userid, tobacco_cessation):
        payload = self.populateTobacco(tobacco_cessation)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).tobacco_cessation().post(payload)
        return response

    def populateTobacco(self, tobacco_cessation):
        return { "tobacco_cessation":{ "timestamp": tobacco_cessation.timestamp, "utc_offset": tobacco_cessation.utc_offset, "cigarettes_allowed": tobacco_cessation.cigarettes_allowed, "cigarettes_smoked": tobacco_cessation.cigarettes_smoked, "cravings": tobacco_cessation.cravings, "last_smoked": tobacco_cessation.last_smoked },"access_token": self.settings.getAccessToken()}

    #------------
    def updateFitness(self, userid, fitness, id):
        payload = self.populateFitness(fitness)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).fitness(id).put(payload)
        return response

    def updateRoutine(self, userid, routine, id):
        payload = self.populateRoutine(routine)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).routine(id).put(payload)
        return response

    def updateNutrition(self, userid, nutrition, id):
        payload = self.populateNutrition(nutrition)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).nutrition(id).put(payload)
        return response

    def updateSleep(self, userid, sleep, id):
        payload = self.populateSleep(sleep)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).sleep(id).put(payload)
        return response

    def updateWeight(self, userid, weight, id):
        payload = self.populateWeight(weight)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).weight(id).put(payload)
        return response

    def updateDiabetes(self, userid, diabetes, id):
        payload = self.populateDiabetes(diabetes)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).diabetes(id).put(payload)
        return response

    def updateBiometric(self, userid, biometrics, id):
        payload = self.populateBiometrics(biometrics)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).biometrics(id).put(payload)
        return response

    def updateTobaccoCessation(self, userid, tobacco_cessation, id):
        payload = self.populateTobacco(tobacco_cessation)
        response = self.api.organizations(self.settings.getOrgId()).users(userid).tobacco_cessation(id).put(payload)
        return response

    #--------------------Delete
    def deleteFitness(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).fitness(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteRoutine(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).routine(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteNutrition(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).nutrition(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteSleep(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).sleep(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteWeight(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).weight(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteDiabetes(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).diabetes(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteBiometrics(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).biometrics(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

    def deleteTobacco(self, userId, Id):
        response = None
        try:    
            response = self.api.organizations(self.orgId).users(userId).tobacco_cessation(Id).delete(**self.filter_dict)
        except Exception:
            pass
        return response;

        
    

