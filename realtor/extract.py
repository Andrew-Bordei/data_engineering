import requests
import json
import random
import time 
from request_params import URL, create_payload

class Extract: 
    def __init__(self, start_page: int, end_page: int) -> None:
        self.start_page = start_page
        self.end_page = end_page
       
    def build_headers(self, city: str, state_abbr: str, page_num: int) -> dict[str, str]: 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': f'https://www.realtor.com/realestateandhomes-search/{city}_{state_abbr}/pg-{page_num}',
            'content-type': 'application/json',
            'rdc-client-name': 'RDC_WEB_SRP_FS_PAGE',
            'rdc-client-version': '3.0.2247',
            'x-is-bot': 'false',
            'x-rdc-visitor-id': 'fb80ae97-a551-485b-9035-180f85484599',
            'srp-consumer-triggered-request': 'rdc-search-for-sale',
            'Origin': 'https://www.realtor.com',
            'Alt-Used': 'www.realtor.com',
            'Connection': 'keep-alive',
            'Cookie': 'split=n; split_tcv=180; __vst=fb80ae97-a551-485b-9035-180f85484599; __bot=false; s_ecid=MCMID%7C36875384715995806410199041729572697991; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCMID%7C36875384715995806410199041729572697991%7CMCIDTS%7C20344%7CMCAID%7CNONE%7CMCOPTOUT-1757800628s%7CNONE%7CvVersion%7C5.2.0; _lr_env_src_ats=false; __split=36; __rdc_id=rdc-id-f7752523-620f-42de-9af8-95a8b2f64a2b; ajs_anonymous_id=e5ad916a-ba8f-48ed-a6fc-c04a31a5284b; G_ENABLED_IDPS=google; _parsely_visitor={%22id%22:%22pid=8f78c9b4-be78-42b7-888d-05c96a3b6406%22%2C%22session_count%22:2%2C%22last_session_ts%22:1757793404081}; __ssn=1d412847-e9eb-465c-84b1-9dedf1172967; __ssnstarttime=1757000912; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; srchID=4355a5fe3cdb4829bb2db93f26f1684a; criteria=sprefix%3D%252Fnewhomecommunities%26area_type%3Dcity%26city%3DBoise%26pg%3D1%26state_code%3DID%26state_id%3DID%26loc%3DBoise%252C%2520ID%26locSlug%3DBoise_ID%26county_fips%3D16001%26county_fips_multi%3D16001; KP_UIDz-ssn=0Ul9EcpfnUh7hdaNhrkTkiO2wcFPtBlfXRNZQwIfpVqOyaNMJVBE3Qgt7FmMqy2qz5i7fwaKerFLtWpK19CfOE8ssMngfVcBr1QKmXCP6Ppe1NiafKLuGhojogroJIiGUBpHGOLhRh7CtnmWXLwyyIVYjZdXA5qlKqbhbYZ1zCiICugr; KP_UIDz=0Ul9EcpfnUh7hdaNhrkTkiO2wcFPtBlfXRNZQwIfpVqOyaNMJVBE3Qgt7FmMqy2qz5i7fwaKerFLtWpK19CfOE8ssMngfVcBr1QKmXCP6Ppe1NiafKLuGhojogroJIiGUBpHGOLhRh7CtnmWXLwyyIVYjZdXA5qlKqbhbYZ1zCiICugr; _lr_retry_request=true; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.realtor.com/realestateandhomes-search/Arkansas%22%2C%22sref%22:%22https://www.realtor.com/%22%2C%22sts%22:1757793404081%2C%22slts%22:1757696617932}; _parsely_slot_click={%22url%22:%22https://www.realtor.com/realestateandhomes-search/Boise_ID%22%2C%22x%22:270%2C%22y%22:21437%2C%22xpath%22:%22//*[@id=%5C%22__next%5C%22]/div[1]/div[4]/div[6]/div[1]/div[1]/a[1]%22%2C%22href%22:%22https://www.realtor.com/realestateandhomes-search/Boise_ID/pg-2%22}; __bot=false; __vst=8a957e7d-82d6-44bc-83e1-296f9069dff9; split=n; split_tcv=117',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'Priority': 'u=4',
            'TE': 'trailers'
        }
        return headers 

    def request_page(self, url: str, headers: dict[str, str], payload: str) -> dict[str, any]:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
    
    def safely_traverse_dict(self, data: dict[str: any], *keys) -> any:
        for key in keys:
            try:
                data = data[key]
            except (KeyError, TypeError):
                return None
        return data

    def extract_data(self, data: dict[str, any]) -> dict[str, any]: 
        all_houses = []
        data = json.loads(data)

        num_houses = self.safely_traverse_dict(data, 'data', 'home_search', 'count')
        base_path = self.safely_traverse_dict(data, 'data', 'home_search', 'properties')

        if num_houses != None and base_path != None: 
            for house in range(0, num_houses): 
                property_id = self.safely_traverse_dict(base_path[house], 'property_id')
                list_price = self.safely_traverse_dict(base_path[house], 'list_price')
                listing_id = self.safely_traverse_dict(base_path[house], 'listing_id')
                beds = self.safely_traverse_dict(base_path[house], 'description', 'beds')
                baths = self.safely_traverse_dict(base_path[house], 'description', 'baths_consolidated')
                sqft = self.safely_traverse_dict(base_path[house], 'description', 'sqft')
                lot_sqft = self.safely_traverse_dict(base_path[house], 'description', 'lot_sqft')
                year_built = self.safely_traverse_dict(base_path[house], 'description', 'year_built')
                garage_num = self.safely_traverse_dict(base_path[house], 'description', 'garage')
                address_line = self.safely_traverse_dict(base_path[house], 'location', 'address', 'line')
                postal_code = self.safely_traverse_dict(base_path[house], 'location', 'address', 'postal_code')
                state_code = self.safely_traverse_dict(base_path[house], 'location', 'address', 'state_code')
                city = self.safely_traverse_dict(base_path[house], 'location', 'address', 'city')
                advertiser_name = self.safely_traverse_dict(base_path[house], 'advertisers', 0, 'name')
                advertiser_office = self.safely_traverse_dict(base_path[house], 'advertisers', 0, 'office', 'name')
                last_price_change_amount = self.safely_traverse_dict(base_path[house], 'last_price_change_amount')

                house_data = {
                    "property_id": property_id, 
                    "list_price": list_price, 
                    "listing_id": listing_id, 
                    "beds": beds,
                    "baths": baths,  
                    "sqft": sqft, 
                    "lot_sqft": lot_sqft, 
                    "year_built": year_built, 
                    "garage_num": garage_num, 
                    "address_line": address_line, 
                    "postal_code": postal_code,
                    "state_code": state_code, 
                    "city": city, 
                    "advertiser_name": advertiser_name,
                    "advertiser_office": advertiser_office,
                    "last_price_change_amount": last_price_change_amount,
                }
                all_houses.append(house_data)
        return all_houses
    
    def extraction_process(self, city: str, state_abbr: str) -> dict[str, any]:
        all_data = []

        for page in range(self.start_page, self.end_page):
            print(f"Getting data on page: {page}")
            headers = self.build_headers(city, state_abbr, page)
            req_payload = create_payload(city, state_abbr)
            page_data = self.request_page(URL, headers=headers, payload=req_payload)
            data = self.extract_data(page_data)
            all_data.append(data)
            time.sleep(random.uniform(0.25, 5))
        return all_data
