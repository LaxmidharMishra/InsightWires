# util/taxonomy_reader.py
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

class TaxonomyReader:
    def __init__(self):
        self._cache = {}
        self._base_path = "taxonomies"

    def _get_file_path(self, taxonomy_name: str) -> str:
        """Get the JSON file path for a taxonomy"""
        file_mapping = {
            'business_events': 'business_activity.json',
            'companies': 'company_taxonomy.json',
            'industries': 'industry.json',
            'countries': 'country.json',
            'content_type': 'content_type_taxonomy.json',
            'sentiments': 'sentimate_taxonomy.json',
            'source_type': 'source_type_taxonomy.json',
            'languages': 'languages.json'
        }
        
        if taxonomy_name not in file_mapping:
            raise KeyError(f"Taxonomy {taxonomy_name} not found")
            
        return os.path.join(self._base_path, file_mapping[taxonomy_name])

    def load_taxonomy(self, taxonomy_name: str) -> List[Dict[str, Any]]:
        """Load taxonomy data from JSON file"""
        if taxonomy_name in self._cache:
            return self._cache[taxonomy_name]
            
        file_path = self._get_file_path(taxonomy_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache[taxonomy_name] = data
                return data
        except FileNotFoundError:
            raise KeyError(f"Taxonomy file {file_path} not found")

    def search_companies(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search companies by name or URL"""
        data = self.load_taxonomy('companies')
        
        if not name and not url:
            return []
            
        results = []
        for company in data:
            company_name = str(company.get('company_name', ''))
            company_url = str(company.get('company_url', ''))
            
            if name and name.lower() in company_name.lower():
                results.append(company)
            elif url and url.lower() in company_url.lower():
                results.append(company)
                
        return results

    def search_taxonomy(
        self,
        taxonomy_name: str,
        search_term: Optional[str] = None,
        field: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all taxonomy data"""
        return self.load_taxonomy(taxonomy_name)

    def add_company_request(self, company_name: Optional[str] = None, company_url: Optional[str] = None) -> Dict[str, Any]:
        """Add a company request to requested_companies.json"""
        request_file = os.path.join(self._base_path, 'requested_companies.json')
        
        # Create new request entry
        new_request = {
            "company_name": company_name,
            "company_url": company_url,
            "requested_date": datetime.now().isoformat(),
            "status": "pending"
        }
        
        try:
            # Load existing requests
            if os.path.exists(request_file):
                with open(request_file, 'r', encoding='utf-8') as f:
                    requests = json.load(f)
            else:
                requests = []
            
            # Add new request
            requests.append(new_request)
            
            # Save updated requests
            with open(request_file, 'w', encoding='utf-8') as f:
                json.dump(requests, f, indent=2)
            
            return new_request
            
        except Exception as e:
            raise Exception(f"Failed to save company request: {str(e)}")

# Create a singleton instance
taxonomy_reader = TaxonomyReader()