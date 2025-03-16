import requests
from config import HEADERS, CRUNCHBASE_API_KEY
import yfinance as yf

class CompetitorInfoCollector:
    def __init__(self):
        self.headers = HEADERS
        self.api_key = CRUNCHBASE_API_KEY
        if not self.api_key or self.api_key == "your_crunchbase_api_key_here":
            print("Warning: Crunchbase API key not set or invalid")
        self.base_url = "https://api.crunchbase.com/api/v4/entities"

    def get_competitors(self, company_name, max_competitors=3):
        competitor_names = self._identify_competitors(company_name, max_competitors)
        
        if not competitor_names:
            competitor_names = self._get_manual_competitors(company_name, max_competitors)

        competitors = []
        for comp_name in competitor_names:
            comp_info = self._get_competitor_details(comp_name)
            if comp_info and comp_info.get('name'):
                competitors.append(comp_info)

        return competitors

    def _identify_competitors(self, company_name, max_competitors=3):
        try:
            company_uuid = self._get_company_uuid(company_name)
            if not company_uuid:
                return []

            competitors_url = f"{self.base_url}/organizations/{company_uuid}/relationships"
            params = {
                "card_ids": "competitors",
                "user_key": self.api_key
            }
            response = requests.get(competitors_url, params=params)

            if response.status_code == 200:
                data = response.json()
                competitor_names = [
                    competitor["properties"]["name"]
                    for competitor in data.get("data", {}).get("cards", [])
                ]
                return competitor_names[:max_competitors]

            return []
        except Exception as e:
            print(f"Error identifying competitors: {e}")
            return []

    def _get_company_uuid(self, company_name):
        try:
            search_url = f"{self.base_url}/organizations"
            params = {
                "query": company_name,
                "field_ids": "name,identifier",
                "card_ids": "identifier",
                "user_key": self.api_key
            }
            response = requests.get(search_url, params=params)

            if response.status_code == 200:
                data = response.json()
                if data["data"]["cards"]:
                    return data["data"]["cards"][0]["identifier"]["uuid"]
            return None
        except Exception as e:
            print(f"Error getting company UUID: {e}")
            return None

    def _get_competitor_details(self, competitor_name):
        try:
            competitor_uuid = self._get_company_uuid(competitor_name)
            result = {
                "name": competitor_name,
                "market_cap": None,
                "employees": None,
                "industry": None
            }
            
            if competitor_uuid:
                org_url = f"{self.base_url}/organizations/{competitor_uuid}"
                params = {
                    "field_ids": "name,short_description,num_employees_enum,categories",
                    "user_key": self.api_key
                }
                response = requests.get(org_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    properties = data.get("properties", {})
                    
                    if "num_employees_enum" in properties:
                        employees = properties["num_employees_enum"]
                        result["employees"] = employees
                    
                    if "categories" in properties:
                        categories = properties.get("categories", [])
                        if categories:
                            result["industry"] = categories[0].get("name")
            
            try:
                ticker = yf.Ticker(competitor_name.replace(" ", ""))
                info = ticker.info
                if "marketCap" in info and info["marketCap"]:
                    market_cap = info["marketCap"]
                    if market_cap >= 1_000_000_000:
                        result["market_cap"] = f"${market_cap / 1_000_000_000:.2f} billion"
                    elif market_cap >= 1_000_000:
                        result["market_cap"] = f"${market_cap / 1_000_000:.2f} million"
                    else:
                        result["market_cap"] = f"${market_cap:,}"
            except Exception as e:
                pass
                
            return result
        except Exception as e:
            print(f"Error getting competitor details: {e}")
            return {
                "name": competitor_name,
                "market_cap": None,
                "employees": None,
                "industry": None
            }
            
    def _get_manual_competitors(self, company_name, max_competitors=3):
        company_name = company_name.lower().strip()
        competitors_map = {
            "microsoft": ["Apple", "Google", "Amazon", "IBM"],
            "apple": ["Samsung", "Google", "Microsoft", "Huawei"],
            "amazon": ["Walmart", "Alibaba", "Microsoft", "Google"],
            "google": ["Microsoft", "Apple", "Facebook", "Amazon"],
            "meta": ["Snap", "TikTok", "LinkedIn", "Twitter"],
            "facebook": ["Snap", "TikTok", "LinkedIn", "Twitter"],
            "netflix": ["Disney+", "Amazon Prime", "Hulu", "HBO Max"],
            "tesla": ["Ford", "General Motors", "Toyota", "Volkswagen"],
            "nvidia": ["AMD", "Intel", "Qualcomm", "ARM"],
            "ibm": ["Microsoft", "Oracle", "SAP", "Amazon"],
            "oracle": ["SAP", "Microsoft", "IBM", "Salesforce"],
        }
        
        if company_name in competitors_map:
            return competitors_map[company_name][:max_competitors]
        return []