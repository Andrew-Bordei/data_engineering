from rnet import Impersonate, Client 
import asyncio 
import json 
from datetime import datetime

async def main():
    url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Boise%2C+ID&radius=25&refine_by_employment=employment_type%3Aall"

    # url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Grand+Rapids%2C+MI&radius=25&refine_by_employment=employment_type%3Aall"

    # url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Harrisburg%2C+PA&radius=25&refine_by_employment=employment_type%3Aall"

    client = Client(impersonate=Impersonate.Chrome137)

    resp = await client.get(url)

    data = await resp.json()

    date = datetime.today().strftime('%Y-%m-%d')

    with open(f'zip_data_boise_{date}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return data 

if __name__ == "__main__":
    print(asyncio.run(main()))
