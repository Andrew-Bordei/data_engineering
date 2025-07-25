import requests
from headers import HEADERS
import random

class Session:
    def __init__(self, headers) -> None:
        # self.payload = payload
        self.user_agent = random.randint(0,10)
        self.headers = headers
        self.headers['User-Agent'] = HEADERS[self.user_agent].get('User-Agent')
        self.session = requests.Session()

    def return_data_safely(self, resp: requests.Session) -> dict:
        if resp.status_code == 200:
            return resp.text
        return None 
    
    def zillow_get_page(self, url: str, headers: dict[str, str], payload: dict) -> dict:
        """Return the house listings for a specific page""" 
        response = self.session.put(url, headers=headers, data=payload)

        return self.return_data_safely(response)
    