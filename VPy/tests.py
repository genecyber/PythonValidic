import unittest
import slumber
import mock
import configController
import slumber.serialize
import unittest
import requests
import slumber
import slumber.serialize
from VPy import Client
import Activity
from Activity import Profile
from Activity import Fitness
from Activity import Routine
from Activity import Nutrition
from Activity import Sleep
from Activity import Weight
from Activity import Diabetes
from Activity import Biometrics
from Activity import TobaccoCessation

class ValidicSpecificTests(unittest.TestCase):
    #===============Settings
    client = Client()    
    settings = client.init("test")
    api =  slumber.API("https://api.validic.com/v1/")
    orgId = settings.getOrgId()
    token = settings.getAccessToken()
    user = settings.getUser()

    def setUp(self):
        self.base_resource = slumber.Resource(base_url="http://api.validic.com/api/v1/organizations/"+ self.settings.getOrgId(), format="json", append_slash=False, access_token = self.settings.getAccessToken())
        settings = self.client.init("enterprise")
        self.client.deleteAllUsers()

    def test_OrganizationInfoQuery(self):
        resp = self.api.organizations(self.orgId).get(access_token = self.token)
        if (self.settings.mode == "test"):
            self.assertEqual(resp["organization"]["name"].encode('utf-8') ,'ACME Corp')

    def test_OrganizationInfoQuery_Live(self):
        self.client.init("live")
        resp = self.api.organizations(self.orgId).get(access_token = self.token)
        if (self.settings.mode == "live"):
            self.assertEqual(resp["organization"]["name"].encode('utf-8') ,'Shannon Code Partner')

    def test_Client_MyOrganizationInfoQuery(self):
        resp = self.client.getMyOrganizationInfo()
        if (self.settings.mode == "test"):
            self.assertEqual(resp["organization"]["name"].encode('utf-8') ,'Shannon Code Partner')

    def test_Client_MyOrganizationInfoQuery_Live(self):
        self.client.init("live")
        resp = self.client.getMyOrganizationInfo()
        if (self.settings.mode == "live"):
            self.assertEqual(resp["organization"]["name"].encode('utf-8') ,'Shannon Code Partner')

    def test_UsersQuery(self):
        resp = self.api.organizations(self.orgId).users.get(access_token = self.token)
        self.assertGreater(len(resp["users"]),1)

    def test_Client_UsersQuery(self):    
        settings = self.client.init("enterprise")
        userResponse = self.client.addUser("query2")
        userResponse = self.client.addUser("query3")
        userResponse = self.client.addUser("query0")
        resp = self.client.getMyUsers()
        self.user = resp["users"][0]["_id"]
        self.assertGreater(len(resp["users"]),1)

    def test_Client_UserQuery(self):
        userResponse = self.client.addUser("query")
        response = self.client.getUser(userResponse["user"]["_id"])
        self.assertIsNotNone(response)

    def test_Client_ResetUserToken(self):
        userResponse = self.client.addUser("reset")
        response = self.client.refreshUserAccessToken(userResponse["user"]["_id"])
        self.assertIsNotNone(response)
        self.assertEqual(response["uid"].encode('utf-8'),"reset")

    def test_Client_SuspendUser(self):   
        userResponse = self.client.addUser("unsuspend")     
        response = self.client.suspendUser(userResponse["user"]["_id"])   
        self.assertIsNotNone(response)
        self.assertEqual(response["message"].encode('utf-8'),"The user has been suspended successfully")

    def test_Client_UnSuspendUser(self):     
        userResponse = self.client.addUser("unsuspend")
        response = self.client.unSuspendUser(userResponse["user"]["_id"])   
        self.assertIsNotNone(response)
        self.assertEqual(response["message"].encode('utf-8'),"The user has been unsuspended successfully")    

    def test_Client_StorefrontUrl(self):
        settings = self.client.init("enterprise")
        userResponse = self.client.addUser("profile")
        response = self.client.refreshUserAccessToken(userResponse["user"]["_id"])

        self.assertIsNotNone(response)
        token = response["authentication_token"]
        response = self.client.getUserStorefrontUrl(token)
        expected = "https://app.validic.com/"+settings.getOrgId()+"/"+token.encode('utf-8')
        self.assertEqual(response.encode('utf-8'),expected)
    
    def test_Client_UserProfile(self):
        #Note: Sending both the org token and the user access token returns weird profiles

        userResponse = self.client.addUser("profile")
        response = self.client.getUser(userResponse["user"]["_id"])

        tokenresp = self.client.refreshUserAccessToken(userResponse["user"]["_id"])
        userResponse = self.client.addUser("reset")
        response = self.client.getUser(userResponse["user"]["_id"])
        token = tokenresp["authentication_token"].encode('utf-8')
        profileresp = self.client.getUserProfile(token)
        self.assertIsNotNone(profileresp)
        self.assertEqual(profileresp["uid"],"profile")

    def test_Client_getFitness(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getFitness(self.user)
        self.assertIsNotNone(response)

    def test_Client_getRoutine(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getRoutine(self.user)
        self.assertIsNotNone(response)

    def test_Client_getNutrition(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getNutrition(self.user)
        self.assertIsNotNone(response)

    def test_Client_getSleep(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getSleep(self.user)
        self.assertIsNotNone(response)

    def test_Client_getWeight(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getWeight(self.user)
        self.assertIsNotNone(response)

    def test_Client_getDiabetesMeasurements(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getDiabetesMeasurements(self.user)
        self.assertIsNotNone(response)

    def test_Client_getBiometricMeasurements(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getBiometricMeasurements(self.user)
        self.assertIsNotNone(response)

    def test_Client_getTobaccoCessation(self):
        response = self.client.addUser("activity")
        self.user = response["user"]["_id"]
        response = self.client.getTobaccoCessation(self.user)
        self.assertIsNotNone(response)
class ValidicAddTests(unittest.TestCase):
     #===============Settings
    client = Client()    
    settings = client.init("enterprise")
    api =  slumber.API("https://api.validic.com/v1/")
    orgId = settings.getOrgId()
    token = settings.getAccessToken()
    user = settings.getUser()

    def setUp(self):
        settings = self.client.init("enterprise")
        self.client.deleteAllUsers()

    def test_Client_ProvisionUser(self):
        uid = "testUIDuid"
        response = self.client.addUser(uid)

    def test_Client_ProvisionUserAndProfile(self):
        uid = "fooId"
        profile = Profile()    
        profile.gender = "F"   
        response = self.client.addUserWithProfile(uid, profile)
        self.assertEqual(response["user"]["profile"]["gender"].encode('utf-8'),"F")

    def test_addFitness(self):
        response = self.client.addUser("fitness")
        fitness = Fitness()
        response = self.client.addFitness(response["user"]["_id"].encode('utf-8'),fitness)
        self.assertEqual(response["fitness"]["type"].encode('utf-8'),fitness.type)

    def test_addRoutine(self):
        response = self.client.addUser("routine")
        routine = Routine()
        routine.floors = 16
        response = self.client.addRoutine(response["user"]["_id"].encode('utf-8'), routine)
        self.assertEqual(response["routine"]["floors"],16)

    def test_addNutrition(self):
        response = self.client.addUser("nutrition")
        nutrition = Nutrition()
        response = self.client.addNutrition(response["user"]["_id"].encode('utf-8'), nutrition)
        self.assertEqual(response["nutrition"]["timestamp"].encode('utf-8'),nutrition.timestamp)

    def test_addSleep(self):
        response = self.client.addUser("sleep")
        sleep = Sleep()
        response = self.client.addSleep(response["user"]["_id"].encode('utf-8'), sleep)
        self.assertEqual(response["sleep"]["timestamp"].encode('utf-8'),sleep.timestamp)

    def test_addWeight(self):
        response = self.client.addUser("weight")
        weight = Weight()
        response = self.client.addWeight(response["user"]["_id"].encode('utf-8'), weight)
        self.assertEqual(response["weight"]["timestamp"].encode('utf-8'),weight.timestamp)

    def test_addDiabetes(self):
        response = self.client.addUser("diabetes")
        diabetes = Diabetes()
        response = self.client.addDiabetes(response["user"]["_id"].encode('utf-8'), diabetes)
        self.assertEqual(response["diabetes"]["timestamp"].encode('utf-8'),diabetes.timestamp)

    def test_addBiometrics(self):
        response = self.client.addUser("biometrics")
        biometrics = Biometrics()
        response = self.client.addBiometrics(response["user"]["_id"].encode('utf-8'), biometrics)
        self.assertEqual(response["biometrics"]["timestamp"].encode('utf-8'),biometrics.timestamp)

    def test_addTobacco(self):
        response = self.client.addUser("tobacco_cessation")
        tobacco_cessation = TobaccoCessation()
        response = self.client.addTobaccoCessation(response["user"]["_id"].encode('utf-8'), tobacco_cessation)
        self.assertEqual(response["tobacco_cessation"]["timestamp"].encode('utf-8'),tobacco_cessation.timestamp)
class UtilsTests(unittest.TestCase):
    client = Client()    
    settings = client.init("test")

    def test_url_join_http(self):
        self.assertEqual(slumber.url_join("http://api.validic.com/"), "http://api.validic.com/")
        self.assertEqual(slumber.url_join("http://api.validic.com/", "v1"), "http://api.validic.com/v1")
        self.assertEqual(slumber.url_join("http://api.validic.com/", "v1", "organizations"), "http://api.validic.com/v1/organizations")

        self.assertEqual(slumber.url_join("http://api.validic.com"), "http://api.validic.com/")
        self.assertEqual(slumber.url_join("http://api.validic.com", "v1"), "http://api.validic.com/v1")
        self.assertEqual(slumber.url_join("http://api.validic.com", "v1", "organizations"), "http://api.validic.com/v1/organizations")

    def test_url_join_https(self):
        self.assertEqual(slumber.url_join("https://api.validic.com/"), "https://api.validic.com/")
        self.assertEqual(slumber.url_join("https://api.validic.com/", "v1"), "https://api.validic.com/v1")
        self.assertEqual(slumber.url_join("https://api.validic.com/", "v1", "organizations"), "https://api.validic.com/v1/organizations")

        self.assertEqual(slumber.url_join("https://api.validic.com"), "https://api.validic.com/")
        self.assertEqual(slumber.url_join("https://api.validic.com", "v1"), "https://api.validic.com/v1")
        self.assertEqual(slumber.url_join("https://api.validic.com", "v1", "organizations"), "https://api.validic.com/v1/organizations")

    def test_url_join_http_port(self):
        self.assertEqual(slumber.url_join("http://api.validic.com:80/"), "http://api.validic.com:80/")
        self.assertEqual(slumber.url_join("http://api.validic.com:80/", "v1"), "http://api.validic.com:80/v1")
        self.assertEqual(slumber.url_join("http://api.validic.com:80/", "v1", "organizations"), "http://api.validic.com:80/v1/organizations")

    def test_url_join_https_port(self):
        self.assertEqual(slumber.url_join("https://api.validic.com:443/"), "https://api.validic.com:443/")
        self.assertEqual(slumber.url_join("https://api.validic.com:443/", "v1"), "https://api.validic.com:443/v1")
        self.assertEqual(slumber.url_join("https://api.validic.com:443/", "v1", "organizations"), "https://api.validic.com:443/v1/organizations")

    def test_url_join_path(self):
        self.assertEqual(slumber.url_join("/"), "/")
        self.assertEqual(slumber.url_join("/", "v1"), "/v1")
        self.assertEqual(slumber.url_join("/", "v1", "organizations"), "/v1/organizations")

        self.assertEqual(slumber.url_join("/v1/"), "/v1/")
        self.assertEqual(slumber.url_join("/v1/", "organizations"), "/v1/organizations")
        self.assertEqual(slumber.url_join("/v1/", "organizations", self.settings.getOrgId()), "/v1/organizations/"+self.settings.getOrgId())

    def test_url_join_trailing_slash(self):
        self.assertEqual(slumber.url_join("http://api.validic.com/", "v1/"), "http://api.validic.com/v1/")
        self.assertEqual(slumber.url_join("http://api.validic.com/", "v1/", "organizations/"), "http://api.validic.com/v1/organizations/")

    def test_url_join_encoded_unicode(self):
        expected = "http://api.validic.com/t?st/"

        url = slumber.url_join("http://api.validic.com/", "t?st/")
        self.assertEqual(url, expected)

        url = slumber.url_join("http://api.validic.com/", "t?st/".decode('utf8').encode('utf8'))
        self.assertEqual(url, expected)

    def test_url_join_decoded_unicode(self):
        url = slumber.url_join("http://api.validic.com/", "t?st/".decode('utf8'))
        expected = "http://api.validic.com/t?st/".decode('utf8')
        self.assertEqual(url, expected)
class ResourceTests(unittest.TestCase):
        client = Client()    
        settings = client.init("test")
        def test_serializer(self):
            s = slumber.serialize.Serializer()

            for content_type in [
                                "application/json",
                                "application/x-javascript",
                                "text/javascript",
                                "text/x-javascript",
                                "text/x-json",
                            ]:
                serializer = s.get_serializer(content_type=content_type)
        
        def setUp(self):
            self.base_resource = slumber.Resource(base_url="http://api.validic.com/api/v1/organizations/"+ self.settings.getOrgId(), format="json", append_slash=False, access_token = self.settings.getAccessToken())

            self.settings = configController.configClient("test")

        def test_get_200_json(self):
            r = mock.Mock(spec=requests.Response)
            r.status_code = 200
            r.headers = {"content-type": "application/json"}
            r.content = '{"summary":{"status":200,"message":"Ok","results":1,"start_date":null,"end_date":null,"offset":0,"limit":100,"params":{"start_date":null,"end_date":null,"offset":null,"limit":null,"source":null}},"organization":{"_id":"51aca5a06dedda916400002b","name":"ACME Corp","users":78,"users_provisioned":514,"activities":197527,"connections":317,"organizations":[]}}'

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.return_value = r

            resp = self.base_resource._request("GET")

            self.assertTrue(resp is r)
            self.assertEqual(resp.content, r.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "GET",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.get()
            self.assertEqual(resp['summary'], {u'status': 200, u'end_date': None, u'results': 1, u'limit': 100, u'offset': 0, u'params': {u'source': None, u'limit': None, u'start_date': None, u'end_date': None, u'offset': None}, u'message': u'Ok', u'start_date': None})

        def getBaseUrl(self):
            return "http://api.validic.com/api/v1/organizations/"+ self.settings.getOrgId()

        def test_get_200_text(self):
            r = mock.Mock(spec=requests.Response)
            r.status_code = 200
            r.headers = {"content-type": "text/plain"}
            r.content = "Mocked Content"

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.return_value = r

            resp = self.base_resource._request("GET")

            self.assertTrue(resp is r)
            self.assertEqual(resp.content, "Mocked Content")

            self.base_resource._store["session"].request.assert_called_once_with(
                "GET",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.get()
            self.assertEqual(resp, r.content)

        def test_post_201_redirect(self):
            r1 = mock.Mock(spec=requests.Response)
            r1.status_code = 201
            r1.headers = {"location": self.getBaseUrl()+"/1"}
            r1.content = ''

            r2 = mock.Mock(spec=requests.Response)
            r2.status_code = 200
            r2.headers = {"content-type": "application/json"}
            r2.content = '{"result": ["a", "b", "c"]}'

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.side_effect = (r1, r2)

            resp = self.base_resource._request("POST")

            self.assertTrue(resp is r1)
            self.assertEqual(resp.content, r1.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "POST",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.post(data={'foo': 'bar'})
            self.assertEqual(resp['result'], ['a', 'b', 'c'])

        def test_post_decodable_response(self):
            r = mock.Mock(spec=requests.Response)
            r.status_code = 200
            r.content = '{"result": ["a", "b", "c"]}'
            r.headers = {"content-type": "application/json"}

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.return_value = r

            resp = self.base_resource._request("POST")

            self.assertTrue(resp is r)
            self.assertEqual(resp.content, r.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "POST",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.post(data={'foo': 'bar'})
            self.assertEqual(resp['result'], ['a', 'b', 'c'])

        def test_patch_201_redirect(self):
            r1 = mock.Mock(spec=requests.Response)
            r1.status_code = 201
            r1.headers = {"location": self.getBaseUrl()+"/1"}
            r1.content = ''

            r2 = mock.Mock(spec=requests.Response)
            r2.status_code = 200
            r2.headers = {"content-type": "application/json"}
            r2.content = '{"result": ["a", "b", "c"]}'

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.side_effect = (r1, r2)

            resp = self.base_resource._request("PATCH")

            self.assertTrue(resp is r1)
            self.assertEqual(resp.content, r1.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "PATCH",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.patch(data={'foo': 'bar'})
            self.assertEqual(resp['result'], ['a', 'b', 'c'])

        def test_patch_decodable_response(self):
            r = mock.Mock(spec=requests.Response)
            r.status_code = 200
            r.content = '{"result": ["a", "b", "c"]}'
            r.headers = {"content-type": "application/json"}

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.return_value = r

            resp = self.base_resource._request("PATCH")

            self.assertTrue(resp is r)
            self.assertEqual(resp.content, r.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "PATCH",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.patch(data={'foo': 'bar'})
            self.assertEqual(resp['result'], ['a', 'b', 'c'])

        def test_put_201_redirect(self):
            r1 = mock.Mock(spec=requests.Response)
            r1.status_code = 201
            r1.headers = {"location": self.getBaseUrl()+"/1"}
            r1.content = ''

            r2 = mock.Mock(spec=requests.Response)
            r2.status_code = 200
            r2.headers = {"content-type": "application/json"}
            r2.content = '{"result": ["a", "b", "c"]}'

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.side_effect = (r1, r2)

            resp = self.base_resource._request("PUT")

            self.assertTrue(resp is r1)
            self.assertEqual(resp.content, r1.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "PUT",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.put(data={'foo': 'bar'})
            self.assertEqual(resp['result'], ['a', 'b', 'c'])

        def test_put_decodable_response(self):
            r = mock.Mock(spec=requests.Response)
            r.status_code = 200
            r.content = '{"result": ["a", "b", "c"]}'
            r.headers = {"content-type": "application/json"}

            self.base_resource._store.update({
                "session": mock.Mock(spec=requests.Session),
                "serializer": slumber.serialize.Serializer(),
            })
            self.base_resource._store["session"].request.return_value = r

            resp = self.base_resource._request("PUT")

            self.assertTrue(resp is r)
            self.assertEqual(resp.content, r.content)

            self.base_resource._store["session"].request.assert_called_once_with(
                "PUT",
                self.getBaseUrl(),
                data=None,
                files=None,
                params=None,
                headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
            )

            resp = self.base_resource.put(data={'foo': 'bar'})
            self.assertEqual(resp['result'], ['a', 'b', 'c'])

        def test_handle_serialization(self):
            self.base_resource._store.update({
                "serializer": slumber.serialize.Serializer(),
            })

            resp = mock.Mock(spec=requests.Response)
            resp.headers = {"content-type": "application/json; charset=utf-8"}
            resp.content = '{"foo": "bar"}'

            r = self.base_resource._try_to_serialize_response(resp)

            if not isinstance(r, dict):
                self.fail("Serialization did not take place")