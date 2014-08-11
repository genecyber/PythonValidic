class Summary(object):
    def __init__(self, action, method, data):
        self.action = action
        self.method = method
        self.data = data

import json

def as_payload(dct):
    return Summary(dct['action'], dct['method'], dct['data'])

payload = json.loads(message, object_hook = as_payload)


{  
   "summary":{  
      "status":200,
      "message":"Ok",
      "results":1,
      "start_date":null,
      "end_date":null,
      "offset":0,
      "limit":100,
      "params":{  
         "start_date":null,
         "end_date":null,
         "offset":null,
         "limit":null,
         "source":null
      }
   },
   "organization":{  
      "_id":"51aca5a06dedda916400002b",
      "name":"ACME Corp",
      "users":78,
      "users_provisioned":514,
      "activities":197527,
      "connections":317,
      "organizations":[  

      ]
   }
}
