from rnet import Impersonate, Client 

class Extract:
    async def extract_data(self, url: str): 
        client = Client(impersonate=Impersonate.Chrome137)

        resp = await client.get(url)
        data = await resp.json()

        return data 
