import requests
import json
import os

# lokal funktion for visualising and debugging json
def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

class NotionSync:
    NOTION_URL = None
    DATABASE_ID = None
    POST_URL = None
    TOKEN = None

    def __init__(self):
        # LOAD PRESETS FROM JSON FILE
        with open(os.path.join(os.path.dirname(__file__), 'pm_settings.json')) as f:
            presets = json.load(f)
        self.NOTION_URL = presets["NOTION_URL"]
        self.DATABASE_ID = presets["DATABASE_ID"]
        self.POST_URL = presets["POST_URL"]
        self.TOKEN = presets["TOKEN"]
        pass    

    def get_headers(self):
        headers = {
            "Authorization": f"{self.TOKEN}",
            "Content-Type": "application/json"
        }
        return headers

    def query_databases(self, payload):
        database_url = self.NOTION_URL + self.DATABASE_ID + "/query"
        response = requests.post(database_url, headers=self.get_headers(), json=payload)
        if response.status_code != 200:
            raise ApiError(f'Response Status: {response.status_code}')
        else:
            return response.json()

    def get_field_names(self,data_json):
        return list(data_json["results"][0]["properties"].keys())

    def get_results(self,data):
        return (data["results"])

    def get_entry(self, payload):
        filter = {
            "filter": {
                "or": [
                    {
                        "property": "NID",
                        "text": {"equals": payload["NID"]}
                    }
                ]
            }
        }
        query = self.query_databases(filter)
        if query.get('results') == None:
             return None
        
        results = query.get('results')
        results = results[0]["properties"]

        out = {}
        for key in results.keys():
            
            if results[key]["type"] == "title":
                out[key] = results[key]["title"][0]["plain_text"]
            elif results[key]["type"] == "rich_text":
                if len(results[key]["rich_text"]) > 0:
                    out[key] = results[key]["rich_text"][0]["text"]["content"]
                else: 
                    out[key] = ""
            elif results[key]["type"] == "select":
                out[key] = results[key]["select"]["name"]
            elif results[key]["type"] == "created_time":
                # print(results[key]["created_time"])
                out[key] = results[key]["created_time"]
            elif results[key]["type"] == "number":
                out[key] = results[key]["number"]
            elif results[key]["type"] == "relation":
                out_val = None
                if len(results[key]["relation"]) > 0:
                    # try to resolve the RELATION
                    ID = results[key]["relation"][0]["id"]
                    url = self.POST_URL + ID
                    response = requests.request("GET", url, headers=self.get_headers(), data={})
                    json = response.json()
                    for key2 in json["properties"].keys():
                        if (json["properties"][key2]["type"] == "title"):
                            el = json["properties"][key2]
                            if len(el["title"]) > 0:
                                out_val = el["title"][0]["plain_text"]

                out[key] = out_val

            # elif results[key]["type"] == "files":
                # print(results[key]["files"])
                # out.append({key: results[key]["created_time"]})
            else:
                out[key] = None
                ## FORDEBUGGIN
                # print("not supported type: "+ results[key]["type"] + " for " +  key)
                some_error_occured = True
        return out

    # UPDATE ENTRY
    def add_entry(self, payload):
        # ADD SOME DATA
        data = {
            "parent": {
                "self.DATABASE_ID": self.DATABASE_ID
            },
            "properties": self.make_properties(payload)
        } 
        if payload.get('self.DATABASE_ID') != None:
            data["parent"]["self.DATABASE_ID"] = payload.get('self.DATABASE_ID')

        # pp_json(data)
        response = requests.request("POST", self.POST_URL, headers=self.get_headers(), json=data)
        res = response.json()
        # NOW MODIFY THE RESULT   
        update_success = self.update_entry(res["id"], {"NID": res["id"]})

        if update_success == 200:
            return res["id"]
        else:
            return None
    
    # UPDATE ENTRY
    def update_entry(self, id, payload):
        json = self.make_properties(payload)
        # pp_json(json)
        response = requests.request("PATCH", self.POST_URL + id, headers=self.get_headers(), json={"properties": json})
        return response.status_code

    # MAKE_PROPERTY
    def make_properties(self, payload):
        properties = {}
        # print(payload.keys())
        for p in payload.keys():
            prop = self.property_struct(p, payload[p])
            if prop != None:
                properties[p] = prop
        return properties
        
    def property_struct(self,key, payload):
        # print(key + ": " + payload)
        result = None
        
        if key == 'NID' or key == 'subject_id':
            return {
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": payload}
                    }
                ]
            }
        elif key == "folder" or key == "notes" or key == "description" or key == "absolute_path":
            return {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": payload}
                        }
                    ]
                }
        elif key == 'status':
            return {
                "type": "select",
                "select": {"name": payload}
            }
        elif key == 'files':
            res =  {
                "type": "files",
                "files": []
            }
            for p in payload: 
                res["files"].append({"name": p, "link": None})
            return res

        return None

        

# # MAIN FUNCTIONS
nsync = NotionSync()
# data = nsync.query_databases({})
# pp_json(data)
# # # FIELDNAMES
# # field_names = nsync.get_field_names(data)
# # # pp_json(field_names)

# # # RESULTS
# # results = nsync.get_results(data)
# # pp_json(results)

# # # ADD ENTRY
# # nsync.add_entry({"folder": "12fjlkeje"})

# # pp_json(nsync.make_properties({"NID": "lskdjfklej"}))

res = nsync.get_entry({"NID": "606e69c1-dcfd-4b13-bdd3-42e01866b2b7"})
pp_json(res)