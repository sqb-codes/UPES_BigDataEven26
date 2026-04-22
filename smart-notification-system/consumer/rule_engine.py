def evaluate_event(event):
    event_type = event.get("event_type")
    amount = event.get("amount", 0)
    location = event.get("location", "unknown")

    # RULE 1: Ignore very small transactions
    if event_type == "transaction" and amount < 100:
        return {
            "priority": "IGNORE",
            "reason": "Transaction amount is too small"
        }
    # RULE 2: Low priority transactions
    elif event_type == "transaction" and amount < 1000:
        return {
            "priority": "LOW",
            "reason": "Normal Transaction"
        }
    # RULE 3: Medium priority transactions
    elif event_type == "transaction" and amount < 10000:
        return {
            "priority": "MEDIUM",
            "reason": "Moderate Transaction amount"
        }
    # RULE 4: High priority transactions
    elif event_type == "transaction" and amount < 50000:
        return {
            "priority": "HIGH",
            "reason": "High Value Transaction amount"
        }
    # RULE 5: Login from unusual location
    elif event_type == "login" and location not in ["Dehradun", "Delhi"]:
        return {
            "priority": "HIGH",
            "reason": "Login from unusual location"
        }
    else:
        return {
            "priority": "LOW",
            "reason": "General Activity"
        }








