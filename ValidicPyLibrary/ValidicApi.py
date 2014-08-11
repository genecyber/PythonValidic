import drest
import configController
import json

class Client():

    def __init__(self,mode):
        self.mode = mode
        self.config = configController.configClient(mode)
        self.api = self.getApiWithParams(dict(access_token=self.config.getAccessToken()))
    # Or even more so:

    def getApiWithParamsCustom(this,params):
        class MySerializationHandler(drest.serialization.SerializationHandler):
            def serialize(self, data_dict):
                # do something to serialize data dictionary
                pass

            def deserialize(self, serialized_data):
                self.data = json.loads(serialized_data)
                pass

        class MyResponseHandler(drest.response.ResponseHandler):
            def __init__(self, status, data, **kw):
                super(MyResponseHandler, self).__init__(status, data, **kw)
                # do something to customize the response handler

        class MyRequestHandler(drest.request.RequestHandler):
            class Meta:
                serialization_handler = MySerializationHandler
                response_handler = MyResponseHandler

            def handle_response(self, response):
                # do something to wrape every response
                pass

        class MyResourceHandler(drest.resource.ResourceHandler):
            class Meta:
                request_handler = MyRequestHandler

            def some_custom_function(self, params=None):
                if params is None:
                    params = {}
                # do some kind of custom api call
                return self.api.make_request('GET', 'users.json')
               
        class MyAPI(drest.API):
                class Meta:
                    baseurl = 'https://api.validic.com/v1/organizations/51aca5a06dedda916400002b/'
                    extra_url_params = ""
                    resource_handler = MyResourceHandler
                    request_handler = MyRequestHandler                    
                Meta.extra_url_params = params
        api = MyAPI()
        api.add_resource("fitness")
        api.add_resource("users")
        api.add_resource("user.refresh",path="refresh_token.json")

        return api    

    def getApiWithParams(this,params):  
        class MyAPI(drest.API):
                class Meta:
                    baseurl = 'https://api.validic.com/v1/organizations/51aca5a06dedda916400002b/'
                    extra_url_params = ""                 
                Meta.extra_url_params = params
        api = MyAPI()
        api.add_resource("fitness")
        api.add_resource("users")
        api.add_resource("user.refresh", path="refresh_token.json")

        return api 

    def voidMethod():
        
        pass

    def simpleGet(this):
        # Make calls openly via any HTTP Method, and any path
        # GET http://localhost:8000/api/v1/users/1/
        response = this.api.make_request('GET', 'fitness.json')
        return response

    def getMyId(this):
        this.api.baseurl = "https://api.validic.com/v1/"
        response = this.api.make_request('GET', 'me.json')
        return response

    def hide():
        # Or attach a resource
        api.add_resource('users')

        # Get available resources
        #api.resources
        #>>> ['users', 'projects', 'etc']

        # Get all objects of a resource
        # GET http://localhost:8000/api/v1/users/
        response = api.users.get()

        # Get a single resource with primary key '1'
        # GET http://localhost:8000/api/v1/users/1/
        response = api.users.get(1)

        # Create a resource data dictionary
        user_data = dict(
            username='john.doe',
            password='oober-secure-password',
            first_name='John',
            last_name='Doe',
            )

        # POST http://localhost:8000/api/v1/users/
        response = api.users.post(user_data)

        # Update a resource with primary key '1'
        response = api.users.get(1)
        updated_data = data.copy()
        updated_data['first_name'] = 'John'
        updated_data['last_name'] = 'Doe'

        # PUT http://localhost:8000/api/v1/users/1/
        response = api.users.put(1, updated_data)

        # Patch a resource with primary key '1'
        # PATCH http://localhost:8000/api/v1/users/1/
        response = api.users.patch(1, dict(first_name='Johnny'))

        # Delete a resource with primary key '1'
        # DELETE http://localhost:8000/api/v1/users/1/
        response = api.users.delete(1)
    pass