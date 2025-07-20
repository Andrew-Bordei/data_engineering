import json
import sys 

sys.path.append('./')
from session import Session
from extract import Extract

url = "https://www.zillow.com/async-create-search-page-state"

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Referer': 'https://www.zillow.com/homes/?category=SEMANTIC&searchQueryState=%7B%22filterState%22%3A%7B%22isTownhouse%22%3A%7B%22value%22%3Atrue%7D%2C%22isLotLand%22%3A%7B%22value%22%3Atrue%7D%2C%22isManufactured%22%3A%7B%22value%22%3Atrue%7D%2C%22isMultiFamily%22%3A%7B%22value%22%3Atrue%7D%2C%22isApartment%22%3A%7B%22value%22%3Atrue%7D%2C%22isCondo%22%3A%7B%22value%22%3Atrue%7D%2C%22isSingleFamily%22%3A%7B%22value%22%3Atrue%7D%2C%22isApartmentOrCondo%22%3A%7B%22value%22%3Atrue%7D%2C%22isRecentlySold%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketPreForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByAgent%22%3A%7B%22value%22%3Atrue%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Atrue%7D%2C%22isAuction%22%3A%7B%22value%22%3Atrue%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Atrue%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Atrue%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A3737%7D%5D%2C%22usersSearchTerm%22%3A%22Boise%20ID%20homes%22%7D',
  'Content-Type': 'application/json',
  'Origin': 'https://www.zillow.com',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-GPC': '1',
  'Priority': 'u=4'
}

def get_all_data() -> list[dict[str:any]]:
    all_data = []
    sess = Session(headers=headers)

    for page in range(1, 21):

        payload = json.dumps({
            "searchQueryState": {
                "pagination": {
                "currentPage": page
                },
                "isMapVisible": False,
                "mapBounds": {
                "west": -116.369806,
                "east": -116.043493,
                "south": 43.488708,
                "north": 43.832628
                },
                "usersSearchTerm": "Boise ID homes",
                "regionSelection": [
                {
                    "regionId": 3737
                }
                ],
                "filterState": {
                "sortSelection": {
                    "value": "globalrelevanceex"
                }
                },
                "isListVisible": True
            },
            "wants": {
                "cat1": [
                "listResults"
                ],
                "cat2": [
                "total"
                ]
            },
            "requestId": 2,
            "isDebugRequest": False
        })

        data = sess.zillow_get_page(url=url, headers=headers, payload=payload)
        all_data.append(data)
    return all_data        

def extract_data(data: list[dict[str:any]]):
    ext = Extract()
    all_data = []
    num_pages = len(data)

    for i in range(0, num_pages):
        


if __name__ == '__main__': 
    zillow_data = get_all_data()
    with open('zillow_data_boise_2025_07_20.json', 'w', encoding='utf-8') as f:
        json.dump(zillow_data, f)