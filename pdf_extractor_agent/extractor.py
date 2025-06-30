from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import fitz  # PyMuPDF
import os
import json

def get_txt(fp):
    txt = ""
    try:
        with fitz.open(fp) as d:
            for p in d:
                txt += p.get_text()
    except Exception as e:
        print(f" Can't read {fp}: {e}")
    return txt

def grab_pdfs(path):
    if not os.path.exists(path):
        print(f" Folder '{path}' not found.")
        return

    out = []
    pdfs = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
    if not pdfs:
        print(f" No PDFs in '{path}'.")
    for f in pdfs:
        p = os.path.join(path, f)
        print(f" Reading: {f}")
        txt = get_txt(p)
        if txt.strip():
            out.append({"file": f, "text": txt[:5000]})
        else:
            print(f" Empty or can't read: {f}")

    with open("sebi_financial_structured_output.json", "w", encoding="utf-8") as file:
        json.dump(out, file, indent=2, ensure_ascii=False)
    print(f" Done. Saved {len(out)} items to 'sebi_financial_structured_output.json'.")

def check_chunks(data):
    if not data:
        print(" Nothing to check, skipping LLM part.")
        return

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    ag = Agent(
        role="ChkAgent",
        goal="Check chunks for M&A readiness points.",
        backstory="Goes through SEBI PDF chunks to see if useful for M&A decisions.",
        llm=llm,
        verbose=True
    )

    for i, d in enumerate(data):
        t = Task(
            description=f"Pull out financial points from '{d['file']}' helpful for M&A analysis:\n\n{d['text'][:3000]}",
            expected_output="List clear financial details for M&A go/no-go analysis.",
            agent=ag
        )
        c = Crew(
            agents=[ag],
            tasks=[t],
            verbose=True
        )
        res = c.kickoff()
        print(f"\n Check for {d['file']}:\n{res}\n{'-'*50}")

if __name__ == "__main__":
    path = r"C:\Users\Shreya\OneDrive\Desktop\local_mna_pdfs"
    grab_pdfs(path)

    try:
        with open("sebi_financial_structured_output.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(" File 'sebi_financial_structured_output.json' missing even after grabbing. Check above logs.")
        data = []

    check_chunks(data)
