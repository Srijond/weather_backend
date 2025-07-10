import json
from pathlib import Path


class BdDistrictService:

    def get_district(self):
        BASE_DIR = Path(__file__).resolve().parent
        file_path = BASE_DIR / 'bd_districts.json'
        with open(file_path,'r',encoding='utf-8') as file:
            districts = json.load(file)
            return districts.get("districts")
        
    def get_url(self,lat,long):
        return f'https://api.open-meteo.com/v1/forecast'
    
    def location_info(self,location):
        location_dict = {}
        import pdb;pdb.set_trace()
        for district in self.get_district():
            location_dict[district['name']] = (district['lat'],district['long'])

        return location_dict[location]