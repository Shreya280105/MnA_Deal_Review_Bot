import json
from datetime import datetime
class ReportGeneratorAgent:
    def __init__(self,
                 cleaned_data_path="output/cleaned_deal_data.json",
                 red_flag_path="output/red_flag_results.json"):
        self.cleaned_data_path = cleaned_data_path
        self.red_flag_path = red_flag_path
    def load_data(self):
        with open(self.cleaned_data_path, "r") as f1, open(self.red_flag_path, "r") as f2:
            return json.load(f1), json.load(f2)
    def assess_recommendation(self, red_flags):
        if not red_flags:
            return " Proceed with the deal"
        elif len(red_flags) <= 2:
            return " Investigate further before proceeding"
        else:
            return " Deal not recommended"
    def generate_report(self):
        cleaned_data, red_flags_data = self.load_data()
        final_report = []
        for deal, red_flag_entry in zip(cleaned_data, red_flags_data):
            structured = deal.get("structured_data", {})
            flags = red_flag_entry.get("flags", [])
            recommendation = self.assess_recommendation(flags)
            report = f"""

================= M&A Deal Report #{red_flag_entry['index']} =================
Title       : {deal.get("title")}
URL         : {deal.get("url")}
Date        : {datetime.now().strftime("%Y-%m-%d")}
--- Extracted Key Details ---
Target Company    : {structured.get('target') or 'N/A'}
Deal Value        : {structured.get('deal_value') or 'N/A'}
Deal Type         : {structured.get('deal_type') or 'N/A'}
Announcement Date : {structured.get('announcement_date') or 'N/A'}
Closing Date      : {structured.get('closing_date') or 'N/A'}
Special Terms     : {', '.join(structured.get('special_terms') or ['None'])}
--- Red Flags ---
{chr(10).join(['- ' + flag for flag in flags]) or 'None'}
--- Final Recommendation ---
{recommendation}
=========================================================
"""
            final_report.append(report.strip())
        return "\n\n".join(final_report)
if __name__ == "__main__":
    generator = ReportGeneratorAgent()
    output = generator.generate_report()
    print(output)
