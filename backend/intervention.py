import os
import json
from backend.risk_scorer import get_severity_band
def get_resources(category_counts: dict) -> list:
    with open(os.path.join(os.path.dirname(__file__), "..", "resources", "resource_bank.json"), "r") as f:
        resource_bank = json.load(f)
        band, dominant_category = get_severity_band(category_counts)
    
        if not dominant_category:
            return []
    
        resources = resource_bank["resources"].get(dominant_category, {}).get(band, [])
        return band, dominant_category, resources
    