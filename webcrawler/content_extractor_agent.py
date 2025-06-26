"""
Content Extractor Agent
Uses requests + trafilatura to extract readable text from a list of URLs, even from sites with bot protection.
"""
import requests
import trafilatura
class ContentExtractorAgent:
    def __init__(self):
        pass
    def extract_from_url(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                result = trafilatura.extract(response.text, include_comments=False, include_tables=False)
                return result
            else:
                print(f" HTTP error {response.status_code} for {url}")
                return None
        except Exception as e:
            print(f" Exception while fetching {url}: {e}")
            return None
    def extract_from_url_list(self, url_list):
        extracted_results = {}
        for url in url_list:
            print(f" Fetching: {url}")
            content = self.extract_from_url(url)
            if content:
                print(" Extracted content")
                extracted_results[url] = content
            else:
                print(" Failed to extract content")
        return extracted_results

#test
if __name__ == "__main__":
    urls = [
    "https://www.zendesk.com/newsroom/press-releases/announcement/#georedirect"
]
    agent = ContentExtractorAgent()
    extracted = agent.extract_from_url_list(urls)
    print("\n Extraction Results:")
    for url, text in extracted.items():
        print(f"\n {url}\n{'-'*80}\n{text[:1000]}...\n")
