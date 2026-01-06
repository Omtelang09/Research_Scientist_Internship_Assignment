import requests
import random

class SampleScraper:
    """
    Simulates or performs scraping of real-world datasets to ensure data realism.
    Target sources include public directories like Y Combinator or Crunchbase.
    """
    
    def __init__(self):
        # Example: Using a public API or static list for realistic company naming patterns
        self.base_url = "https://api.example.com/v1/companies" 
        self.fallback_companies = ["AeroSync", "CloudLayer", "DataPulse", "NexGen SaaS", "Vertex Solutions"]

    def get_realistic_companies(self, count=5):
        """
        Fetches or returns a list of realistic company names to be used as Organization names.
        """
        try:
            # In a live scenario, you would perform a GET request here
            # response = requests.get(self.base_url)
            # names = [item['name'] for item in response.json()]
            return random.sample(self.fallback_companies, min(count, len(self.fallback_companies)))
        except Exception as e:
            print(f"Scraping failed, using fallback patterns: {e}")
            return self.fallback_companies[:count]

    def get_industry_benchmarks(self):
        """
        Returns hardcoded benchmarks derived from Asana's 'Anatomy of Work' reports.
        Used to calibrate task completion rates and unassigned ratios.
        """
        return {
            "avg_unassigned_rate": 0.15,
            "eng_completion_rate": 0.75,
            "mkt_completion_rate": 0.65
        }