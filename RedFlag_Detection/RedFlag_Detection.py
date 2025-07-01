from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json
def load_json(f):
    try:
        with open(f, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f" Error loading {f}: {e}")
        return []

def detect_flags(data):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    ag = Agent(
        role="FlagChecker",
        goal="Detect financial red flags and anomalies for M&A readiness.",
        backstory="An expert M&A analyst trained to find hidden issues and unusual patterns in company financials from SEBI/company PDFs using a structured approach.",
        llm=llm,
        verbose=True
    )

    for d in data:
        txt = d.get('content') or d.get('text', '')
        if not txt.strip():
            print(f" Skipping empty file: {d.get('file', 'Unknown')}")
            continue

        t = Task(
            description=f"""Analyze the following extracted financial data and return JSON:
- red_flags: list of red flags detected
- anomalies: list of unusual data points
- notes: additional observations

Data:
{txt[:3000]}""",
            expected_output="JSON with keys: red_flags, anomalies, notes",
            agent=ag
        )
        c = Crew(
            agents=[ag],
            tasks=[t],
            verbose=True
        )
        r = c.kickoff()
        print(f"\n Results for {d.get('file', 'Unknown')}:\n{r}\n{'-'*50}")

if __name__ == "__main__":
    data = load_json("sebi_financial_structured_output.json")
    if data:
        detect_flags(data)
    else:
        print("⚠️ No data found for red flag detection.")
