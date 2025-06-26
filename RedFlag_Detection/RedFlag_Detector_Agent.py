import json
class RedFlagDetectorAgent:
    def __init__(self, filepath="output/cleaned_deal_data.json"):
        self.filepath = filepath
    def load_cleaned_data(self):
        with open(self.filepath, "r") as f:
            return json.load(f)
    def detect_red_flags(self, deal):
        flags = []
        data = deal.get("structured_data", {})
        # Rule 1: Missing target company
        if not data.get("target"):
            flags.append("Missing target company")
        # Rule 2: Missing or same announcement and closing date
        if not data.get("announcement_date"):
            flags.append("Missing announcement date")
        if not data.get("closing_date"):
            flags.append("Missing closing date")
        elif data.get("announcement_date") == data.get("closing_date"):
            flags.append("Announcement and closing date are the same")
        # Rule 3: Deal value unusually high (e.g., > $15B)
        if data.get("deal_value"):
            try:
                val_str = data["deal_value"].lower().replace("$", "").strip()
                if "billion" in val_str:
                    value = float(val_str.replace("billion", "").strip())
                    if value > 15:
                        flags.append("Deal value unusually high")
            except Exception:
                flags.append("Could not interpret deal value")
        # Rule 4: Missing or suspicious deal type
        if not data.get("deal_type"):
            flags.append("Missing deal type")
        # Rule 5: No special terms mentioned
        if not data.get("special_terms"):
            flags.append("No special terms identified")
        return flags
    def run(self):
        deals = self.load_cleaned_data()
        for idx, deal in enumerate(deals, 1):
            print(f"\n--- Deal {idx}: {deal['title']} ---")
            flags = self.detect_red_flags(deal)
            if flags:
                print("Red Flags Detected:")
                for flag in flags:
                    print(" -", flag)
            else:
                print("No red flags found.")
if __name__ == "__main__":
    detector = RedFlagDetectorAgent()
    detector.run()
