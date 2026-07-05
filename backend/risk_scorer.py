def get_severity_band(category_counts: dict) -> tuple:
    total = sum(category_counts.values())
    
    if total < 5:
        band = "minimal"
    elif total < 10:
        band = "mild"
    elif total < 15:
        band = "moderate"
    else:
        band = "severe"
    
    dominant = max(category_counts, key=category_counts.get) if category_counts else None
    
    return band, dominant