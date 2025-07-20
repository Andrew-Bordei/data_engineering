from rnet import Impersonate, Client 
import asyncio 
import json 

async def main():
    # url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Boise%2C+ID&radius=25&refine_by_employment=employment_type%3Aall"

    # url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Grand+Rapids%2C+MI&radius=25&refine_by_employment=employment_type%3Aall"

    url = "https://www.ziprecruiter.com/ajax/salary_counts?location=Harrisburg%2C+PA&radius=25&refine_by_employment=employment_type%3Aall"

    client = Client(impersonate=Impersonate.Chrome137)

    resp = await client.get(url)

    data = await resp.json()

    with open('zip_data_harrisburg_2025_07_20.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return data 

if __name__ == "__main__":
    print(asyncio.run(main()))