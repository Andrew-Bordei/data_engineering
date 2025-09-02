import random
import time 
import json
from zillow_session import ZillowSession 


class ZillowExtract:
    def __init__(self, url: str, headers: dict[str,str], MAX_PAGES: int, MIN_SLEEP: float, MAX_SLEEP: int):
        self.url = url 
        self.headers = headers
        self.max_pages = MAX_PAGES
        self.min_sleep = MIN_SLEEP
        self.max_sleep = MAX_SLEEP 

    def get_all_pages(
            self, west_bound: int, east_bound: int, south_bound: int, 
            north_bound: int, search_term: str, region_id: int 
        ) -> list[dict[str,any]]:
        """Iterates through all the pages and gets all data listed on each page"""

        all_data = []
        sess = ZillowSession(headers=self.headers)

        for page in range(1, self.max_pages):
            time.sleep(random.uniform(self.min_sleep, self.max_sleep))
            print(f"Getting the housing data on page: {page}")

            payload = sess.set_payload(page,west_bound,east_bound,south_bound,north_bound,search_term,region_id)
            data = sess.zillow_get_page(url=self.url, headers=self.headers, payload=payload)
            all_data.append(data)
        return all_data   
         
    def extract_page_data(self, data: list[dict[str,any]]) -> list[any]:
        """Extract data from each page and store it in a list"""
        
        all_data = []
        num_pages = len(data)

        for i in range(0, num_pages):
            json_data = json.loads(data[i])
            house_data = self.extract_house_data(json_data)
            all_data.append(house_data)
        return all_data
    
    def safely_traverse_dict(self, dict: dict[str: any], *keys) -> any:
        for key in keys:
            try:
                dict = dict[key]
            except KeyError:
                return None
        return dict
    
    def extract_house_data(self, json_data: dict[str:any]) -> list[dict[str:any]]:
        """Extract the data from each house listing"""
        all_houses_data = []
        base_path = json_data['cat1']['searchResults']['listResults']
        num_houses = len(base_path)

        for house in range(0, num_houses):
            home_info_path = base_path[house]['hdpData']['homeInfo']

            house_id = self.safely_traverse_dict(base_path[house], 'id')
            address = self.safely_traverse_dict(base_path[house], 'address')
            price = self.safely_traverse_dict(home_info_path, 'price')
            tax_assessed_price = self.safely_traverse_dict(home_info_path, 'taxAssessedValue')
            bedrooms = self.safely_traverse_dict(home_info_path, 'bedrooms')
            bathrooms = self.safely_traverse_dict(home_info_path, 'bathrooms')
            living_sqft = self.safely_traverse_dict(home_info_path, 'livingArea')
            lot_sqft = self.safely_traverse_dict(home_info_path, 'lotAreaValue')
            lot_unit = self.safely_traverse_dict(home_info_path, 'lotAreaUnit')
            days_on_zillow = self.safely_traverse_dict(home_info_path, 'daysOnZillow')
            price_change = self.safely_traverse_dict(home_info_path, 'priceChange')
            date_price_change = self.safely_traverse_dict(home_info_path, 'datePriceChanged')
            zestimate = self.safely_traverse_dict(home_info_path, 'zestimate')
            rent_zestimate = self.safely_traverse_dict(home_info_path, 'rentZestimate')
            home_status = self.safely_traverse_dict(home_info_path, 'homeStatus')
            home_type = self.safely_traverse_dict(home_info_path, 'homeType')
            non_owner_occupied = self.safely_traverse_dict(home_info_path, 'isNonOwnerOccupied')
            preforeclosure_auction = self.safely_traverse_dict(home_info_path, 'isPreforeclosureAuction')
            premier_builder = self.safely_traverse_dict(home_info_path, 'isPremierBuilder')
            marketing_status = self.safely_traverse_dict(base_path[house], 'marketingStatusSimplifiedCd')
            broker = self.safely_traverse_dict(base_path[house], 'brokerName')
            country_currency = self.safely_traverse_dict(base_path[house], 'countryCurrency')

            house_data = {
                "house_id": house_id, 
                "address": address, 
                "price": price,
                "tax_assessed_price": tax_assessed_price,
                "bedrooms": bedrooms, 
                "bathrooms": bathrooms, 
                "living_sqft": living_sqft, 
                "lot_sqft": lot_sqft, 
                "lot_unit": lot_unit, 
                "days_on_zillow": days_on_zillow,
                "price_change": price_change, 
                "date_price_change": date_price_change, 
                "zestimate": zestimate, 
                "rent_zestimate": rent_zestimate,
                "home_status": home_status,
                "home_type": home_type,
                "non_owner_occupied": non_owner_occupied, 
                "preforeclosure_auction": preforeclosure_auction, 
                "premier_builder": premier_builder, 
                "marketing_status": marketing_status, 
                "broker": broker, 
                "country_currency": country_currency
            }
            all_houses_data.append(house_data)
        return all_houses_data
    
    def extract(self,  west_bound: int, east_bound: int, south_bound: int, 
        north_bound: int, search_term: str, region_id: int) -> list[any]:
        """Execute the entire extraction process"""

        all_pages = self.get_all_pages(
            west_bound, east_bound, south_bound, 
            north_bound, search_term, region_id
        )
        
        house_data = self.extract_page_data(all_pages)
        return house_data
