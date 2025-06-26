from search_agent import SearchAgent
from content_extractor_agent import ContentExtractorAgent
from cleaner_agent import CleanerAgent
import textwrap
import json
import os
if __name__ == "__main__":
    agent = SearchAgent(api_key="5824ff0adb5b939ab80c6070696a1bda2f19135c")
    extractor = ContentExtractorAgent()
    cleaner = CleanerAgent()
    print("Searching for documents...")
    try:
        results = agent.search_company_documents("Zendesk", "M&A acquisition investor news", num_results=3)
        all_structured_data = []
        for idx, result in enumerate(results, 1):
            url = result["link"]
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No Snippet")
            print(f"\nResult {idx}: {title}\nURL: {url}\nSnippet: {snippet}")
            try:
                content = extractor.extract_from_url(url)
                if content:
                    print("\n[DEBUG] Extracted Content Snippet:")
                    print(textwrap.shorten(content, width=200))
                    cleaned_data = cleaner.clean(content)
                    print("\nStructured Extracted Data:")
                    for key, val in cleaned_data.items():
                        print(f"- {key}: {val}")
                    # Only save if at least one key has non-null value
                    if any(val is not None for val in cleaned_data.values()):
                        all_structured_data.append({
                            "url": url,
                            "title": title,
                            "structured_data": cleaned_data
                        })
                else:
                    print("Failed to extract content.")
            except Exception as fetch_error:
                print(f"Exception while processing {url}: {fetch_error}")
        # Write to output JSON file
        os.makedirs("output", exist_ok=True)
        with open("output/cleaned_deal_data.json", "w") as f:
            json.dump(all_structured_data, f, indent=4)
        print("\n Saved structured data to 'output/cleaned_deal_data.json'.")
    except Exception as api_error:
        print("Error:", api_error)
