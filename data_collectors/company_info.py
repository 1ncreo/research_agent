import requests
from bs4 import BeautifulSoup
import re
import json
from config import HEADERS

class CompanyInfoCollector:
    def __init__(self):
        self.headers = HEADERS
    
    def get_company_overview(self, company_name):
        result = {
            "company_name": company_name,
            "headquarters": None,
            "founded": None,
            "industry": None,
            "ceo": None,
            "employees": None,
        }
        
        wiki_data = self._get_from_wikipedia(company_name)
        if wiki_data:
            result.update(wiki_data)
                    
        return result
    
    def _get_from_wikipedia(self, company_name):
        try:
            search_url = f"https://en.wikipedia.org/wiki/{company_name.replace(' ', '_')}"
            response = requests.get(search_url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                infobox = soup.find('table', {'class': 'infobox'})
                
                if infobox:
                    info = {}
                    
                    hq_row = infobox.find('th', string=re.compile('Headquarters|Location'))
                    if hq_row and hq_row.find_next('td'):
                        info['headquarters'] = hq_row.find_next('td').text.strip()
                    
                    founded_row = infobox.find('th', string=re.compile('Founded|Established'))
                    if founded_row and founded_row.find_next('td'):
                        founded_text = founded_row.find_next('td').text.strip()
                        years = re.findall(r'\b(?:19|20)\d{2}\b', founded_text)
                        if years:
                            info['founded'] = int(years[0])
                    
                    industry_row = infobox.find('th', string=re.compile('Industry|Sector'))
                    if industry_row and industry_row.find_next('td'):
                        info['industry'] = industry_row.find_next('td').text.strip()
                    
                    ceo_row = infobox.find('th', string=re.compile('CEO|Chief Executive Officer|Key people|Leadership'))
                    if ceo_row and ceo_row.find_next('td'):
                        ceo_text = ceo_row.find_next('td').text.strip()
                        info['ceo'] = ceo_text.split(',')[0].strip()
                    
                    emp_row = infobox.find('th', string=re.compile('Employees|Number of employees|Staff'))
                    if emp_row and emp_row.find_next('td'):
                        emp_text = emp_row.find_next('td').text.strip()
                        numbers = re.findall(r'[\d,]+', emp_text)
                        if numbers:
                            info['employees'] = numbers[0]
                    
                    return info
                else:
                    return {}
            else:
                return {}
            
            return {}
        except Exception as e:
            return {}