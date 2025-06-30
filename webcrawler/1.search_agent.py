from crewai import Agent, Task, Crew
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
import requests

class SearchAgent:
    def __init__(self, apik):
        self.apik = apik
        self.serper_url = "https://google.serper.dev/search"

    def search(self, query):
        headers = {"X-API-KEY": self.apik, "Content-Type": "application/json"}
        payload = {"q": query, "num": 3}
        r = requests.post(self.serper_url, headers=headers, json=payload)
        if r.status_code == 200:
            results = r.json().get("organic", [])
            return "\n".join([item["link"] for item in results])
        else:
            return f"Serper Error {r.status_code}: {r.text}"

sa = SearchAgent(apik="b4d................................070")

serper = Tool(
    name="serper",
    func=sa.search,  #single string query
    description="Fetch top 3 M&A URLs for a company."
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

a = Agent(
    role="WebSearch",
    goal="Find top M&A URLs for analysis.",
    backstory="Specialist in finding relevant M&A URLs using Serper API.",
    tools=[serper],
    llm=llm,
    verbose=True
)
t = Task(
    description="Find top 3 Zendesk M&A URLs for due diligence.",
    expected_output="A list of 3 relevant URLs for Zendesk M&A news.",
    agent=a
)
crew = Crew(
    agents=[a],
    tasks=[t],
    verbose=True
)

if __name__ == "__main__":
    res = crew.kickoff()
    print(res)
