import requests
import json


class Extract: 
    def __init__(self,):
       

    def build_headers(self): 
        headers = {
            
        }
        return headers 

    def build_url(self, page_num: int):
        url = f""
        return url 
 
    def request_page(self, url: str, headers: dict[str, str]) -> dict[str, any]:
        response = requests.request("GET", url, headers=headers)
        return response.text
    
    def safely_traverse_dict(self, dict: dict[str: any], *keys) -> any:
        for key in keys:
            try:
                dict = dict[key]
            except KeyError:
                return None
        return dict

    def extract_data(self, data: dict[str, any]): 
        all_houses = []
        data = json.loads(data[4:])
        num_houses = len(data['payload']['homes'])

        for house in range(0, num_houses): 
            base_path = data['payload']['homes'][house]

             property_id = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )
             = self.safely_traverse_dict(base_path, )

            house_data = {
                

            }
            all_houses.append(house_data)
        return all_houses
    