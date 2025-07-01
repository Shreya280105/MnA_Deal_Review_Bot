from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json
from fpdf import FPDF

def load_flags(f):
    try:
        with open(f, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {f}: {e}")
        return []
def save_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 8, line)
    pdf.output(filename)
    print(f" Saved PDF report as {filename}")
def gen_report(flags):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    ag = Agent(
        role="ReportWriter",
        goal="Generate a detailed M&A readiness report from red flag data.",
        backstory="An expert M&A report agent creating clear acquisition decision reports.",
        llm=llm,
        verbose=True
    )
    combined_txt = "\n\n".join([f"File: {f['file']}\nResult: {f['result']}" for f in flags])
    t = Task(
        description=f"""Using the extracted red flags and financial anomalies below, generate a detailed acquisition readiness report with sections for:
- Company Overview
- Key Financial Findings
- Identified Red Flags
- Potential Risks
- Recommendations
Data:
{combined_txt[:6000]}
""",
        expected_output="Structured M&A readiness report.",
        agent=ag
    )
    c = Crew(
        agents=[ag],
        tasks=[t],
        verbose=True
    )
    r = c.kickoff()
    report_txt = str(r)  # converting CrewOutput to string

    print("\nGenerated Report Preview:\n", report_txt[:1000], "...\n")
    save_pdf(report_txt, "mna_readiness_report.pdf")
if __name__ == "__main__":
    flags = load_flags("sebi_redflag_output.json")
    if flags:
        gen_report(flags)
    else:
        print(" No flagged data found to generate report.")
