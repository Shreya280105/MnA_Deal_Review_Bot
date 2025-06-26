import re
class CleanerAgent:
    def __init__(self):
        pass
    def clean(self, text):
        return {
            "deal_value": self.extract_deal_value(text),
            "target": self.extract_target(text),
            "deal_type": self.extract_deal_type(text),
            "announcement_date": self.extract_announcement_date(text),
            "closing_date": self.extract_closing_date(text),
            "special_terms": self.extract_special_terms(text)
        }
    def extract_deal_value(self, text):
        match = re.search(r'\$(\d+(\.\d+)?\s?(billion|million))', text, re.IGNORECASE)
        return match.group(0) if match else None
    def extract_target(self, text):
        match = re.search(r'acquire[sd]?\s([A-Z][\w&\s\-]+)', text)
        return match.group(1).strip() if match else None
    def extract_deal_type(self, text):
        types = ['all-cash', 'stock-swap', 'private equity', 'merger']
        for t in types:
            if t in text.lower():
                return t
        return None
    def extract_announcement_date(self, text):
        patterns = [
            r'(?:announced on|dated)\s([A-Z][a-z]+ \d{1,2}, \d{4})',
            r'(?:today announced.*?)\s([A-Z][a-z]+ \d{1,2}, \d{4})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    def extract_closing_date(self, text):
        match = re.search(r'(?:close(?:[ds])?(?: on)?|completion.*?)\s([A-Z][a-z]+ \d{1,2}, \d{4})', text)
        return match.group(1) if match else None
    def extract_special_terms(self, text):
        terms = []
        if 'earnout' in text.lower():
            terms.append("earnout")
        if 'no shop' in text.lower():
            terms.append("no shop clause")
        if 'termination fee' in text.lower():
            terms.append("termination fee")
        if 'privately held' in text.lower():
            terms.append("buyout")
        return terms if terms else None
