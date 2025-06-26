"""
Search Agent using Serper API to fetch relevant URLs for M&A documents and company info.
"""
import requests
class SearchAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.serper_url = "https://google.serper.dev/search"
    def search_company_documents(self, company_name, query, num_results=5):
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": f"{company_name} {query}",
            "num": num_results
        }
        response = requests.post(self.serper_url, headers=headers, json=payload)
        if response.status_code == 200:
            results = response.json().get("organic", [])
            return [r["link"] for r in results]
        else:
            raise Exception(f"Serper API Error: {response.status_code} - {response.text}")

#Test Agent Search
if __name__ == "__main__":
    agent = SearchAgent(api_key="dd17e0b61d50257e5b24cfc6d859514831a3a2b7")
    try:
        urls = agent.search_company_documents("Zendesk", "investor relations M&A", num_results=5)
        print(" Top Search Results:")
        for url in urls:
            print("-", url)
    except Exception as e:
        print(" Error:", e)
