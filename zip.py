from rnet import Impersonate, Client 
import asyncio 
import json 
from datetime import datetime

class Zip:
    def __init__(self, url: str, city: str):
        self.url = url 
        self.city = city

    async def extract_data(self): 
        client = Client(impersonate=Impersonate.Chrome137)

        resp = await client.get(self.url)
        data = await resp.json()

        return data 
    
    def load_data(self, data: dict[str, any]):
        date = datetime.today().strftime('%Y-%m-%d')

        with open(f'zip_data_{self.city}_{date}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

        return 'Data was successfully saved!'

    async def main(self):
        data = await self.extract_data()
        loaded_data = self.load_data(data)

        return loaded_data 
    

if __name__ == "__main__":
    boise_url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Boise%2C+ID&radius=25&refine_by_employment=employment_type%3Aall"
    gr_url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Grand+Rapids%2C+MI&radius=25&refine_by_employment=employment_type%3Aall"
    harrisburg_url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Harrisburg%2C+PA&radius=25&refine_by_employment=employment_type%3Aall"
    
    boise_zip = Zip(boise_url, 'boise')
    gr_zip = Zip(gr_url, 'grand_rapids')
    harrisburg_zip = Zip(harrisburg_url, 'harrisburg')

    async def get_all_data():
        data = await asyncio.gather(
            boise_zip.main(),
            gr_zip.main(),
            harrisburg_zip.main()
        )
        return data 

    all_data = asyncio.run(get_all_data())


