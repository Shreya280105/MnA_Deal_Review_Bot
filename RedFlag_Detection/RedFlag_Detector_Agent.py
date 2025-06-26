import json
import os
class RedFlagDetectorAgent:
    def __init__(self, input_path="output/cleaned_deal_data.json", output_path="output/red_flag_results.json"):
        self.input_path = input_path
        self.output_path = output_path
    def load_cleaned_data(self):
        with open(self.input_path, "r") as f:
            return json.load(f)
    def detect_red_flags(self, data):
        flags = []
        if not data.get("target"):
            flags.append("Missing target company name")
        if not data.get("deal_value"):
            flags.append("Missing deal value")
        if not data.get("announcement_date"):
            flags.append("Missing announcement date")
        if not data.get("closing_date"):
            flags.append("Missing closing date")
        elif data.get("announcement_date") == data.get("closing_date"):
            flags.append("Closing date is the same as announcement date")
        if not data.get("deal_type"):
            flags.append("Missing deal type")
        if not data.get("special_terms"):
            flags.append("No special terms identified")
        return flags
    def run(self):
        deals = self.load_cleaned_data()
        report = []
        for idx, deal in enumerate(deals, 1):
            flags = self.detect_red_flags(deal.get("structured_data", {}))
            report.append({
                "index": idx,
                "title": deal.get("title"),
                "url": deal.get("url"),
                "flags": flags
            })
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"✅ Red flag results saved to {self.output_path}")
if __name__ == "__main__":
    detector = RedFlagDetectorAgent()
    detector.run()
