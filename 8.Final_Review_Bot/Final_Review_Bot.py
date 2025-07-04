import subprocess
import sys
import os

def run_script(file):
    print(f"\n--- Running: {file} ---\n")
    try:
        subprocess.run([sys.executable, file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {file}: {e}")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Extract PDFs
    run_script(os.path.join(base, "sebi_pdf_extractor_agent.py"))

    # Step 2: Detect Red Flags
    run_script(os.path.join(base, "RedFlag_Detection.py"))

    # Step 3: Generate Report
    run_script(os.path.join(base, "Report_Generation.py"))

    print("\n All agents completed successfully. Check your folder for outputs:\n- sebi_financial_structured_output.json\n- sebi_redflag_output.json\n- mna_readiness_report.pdf")
