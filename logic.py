def business_health(revenue, expenses, cash, debtors, creditors):
    profit = revenue - expenses
    profit_margin = profit / revenue if revenue else 0

    burn_rate = expenses - revenue if expenses > revenue else 0
    runway = cash / burn_rate if burn_rate > 0 else float("inf")

    if runway < 3:
        risk = "HIGH"
        advice = "Urgent action needed. Reduce costs or increase revenue immediately."
    elif runway < 6:
        risk = "MEDIUM"
        advice = "Monitor cash closely and improve collections."
    else:
        risk = "LOW"
        advice = "Business is stable, but keep tracking performance."

    return {
        "profit": profit,
        "profit_margin": round(profit_margin * 100, 2),
        "burn_rate": burn_rate,
        "runway": round(runway, 1) if runway != float("inf") else "Stable",
        "risk": risk,
        "advice": advice
    }
