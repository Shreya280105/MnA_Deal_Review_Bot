from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json

def load_json(f):
    try:
        with open(f, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {f}: {e}")
        return []

def detect_flags(data):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    ag = Agent(
        role="FlagChecker",
        goal="Spot financial red flags and anomalies for M&A deals.",
        backstory="M&A analyst agent that spots hidden issues in SEBI/company filings.",
        llm=llm,
        verbose=True
    )

    out = []
    for d in data:
        txt = d.get('content') or d.get('text', '')
        if not txt.strip():
            print(f"Skipping empty: {d.get('file', 'Unknown')}")
            continue

        t = Task(
            description=f"""Check this data and give JSON:
- red_flags: list of red flags
- anomalies: list of unusual items
- notes: extra observations

Data:
{txt[:3000]}""",
            expected_output="JSON with: red_flags, anomalies, notes",
            agent=ag
        )

        c = Crew(
            agents=[ag],
            tasks=[t],
            verbose=True
        )

        r = c.kickoff()
        # Converting CrewOutput to plain text before saving
        result_text = str(r)

        print(f"\n Done for {d.get('file', 'Unknown')}:\n{result_text}\n{'-'*50}")
        out.append({
            "file": d.get('file', 'Unknown'),
            "result": result_text
        })

    with open("sebi_redflag_output.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(" Saved flagged data to 'sebi_redflag_output.json'.")

if __name__ == "__main__":
    data = load_json("sebi_financial_structured_output.json")
    if data:
        detect_flags(data)
    else:
        print(" No data found for red flag detection.")
