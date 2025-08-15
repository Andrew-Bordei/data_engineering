# Rename to ZillowExtract
class Extract:
    def __init__(self):
        pass
    
    # Add to new class 
    def safely_traverse_dict(self, dict: dict[str: any], *keys) -> any:
        for key in keys:
            try:
                dict = dict[key]
            except KeyError:
                return None
        return dict
    
    def zillow_extract_data(self, json_data: dict[str:any]) -> list[dict[str:any]]:
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
