# storage/database.py
import pymongo
from datetime import datetime
from config import MONGO_URI, MONGO_DB

class DatabaseManager:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URI)
            self.db = self.client[MONGO_DB]
            self.companies = self.db.companies
            self.research = self.db.research
            self.connected = True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.client = None
            self.db = None
            self.companies = None
            self.research = None
            self.connected = False
    
    def save_research(self, company_research):
        if not self.connected:
            print("Database not connected. Cannot save research.")
            return False
        
        try:
            # Add timestamp
            company_research['timestamp'] = datetime.now()
            
            # Insert or update
            result = self.research.update_one(
                {"company_name": company_research.get('company_name')},
                {"$set": company_research},
                upsert=True
            )
            
            return True
        except Exception as e:
            print(f"Error saving research: {e}")
            return False
    
    def get_research(self, company_name):
        if not self.connected:
            print("Database not connected. Cannot retrieve research.")
            return None
        
        try:
            result = self.research.find_one(
                {"company_name": company_name},
                sort=[("timestamp", pymongo.DESCENDING)]
            )
            
            if result:
                # Remove MongoDB ID
                if '_id' in result:
                    del result['_id']
                return result
            
            return None
        except Exception as e:
            print(f"Error retrieving research: {e}")
            return None