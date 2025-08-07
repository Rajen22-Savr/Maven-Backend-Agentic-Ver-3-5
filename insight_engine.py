
import pandas as pd

def run_all_insights(df: pd.DataFrame) -> list:
    actions = []

    # Insight 1: High Potential Savings
    df['Potential Savings'] = df['CY Quantity (Fiscal)'] * df['CY vs PY WAP USD (Fiscal)']
    high_savings = df[df['Potential Savings'] > 50000]
    for _, row in high_savings.iterrows():
        actions.append({
            "type": "Renegotiate Pricing",
            "supplier": row["Supplier Name"],
            "savings": round(row["Potential Savings"], 2),
            "action": f"Email to sourcing lead: We've identified an opportunity to renegotiate pricing with {row['Supplier Name']}. Potential savings: ${row['Potential Savings']:,.0f}."
        })

    # Insight 2: Tail Spend Consolidation
    low_spend = df.groupby("Supplier Name")["Total Spend (Fiscal)"].sum()
    tail_suppliers = low_spend[low_spend < 10000]
    if len(tail_suppliers) > 3:
        actions.append({
            "type": "Consolidate Tail Spend",
            "note": f"{len(tail_suppliers)} suppliers under $10K spend.",
            "action": "Initiate sourcing review to consolidate tail spend suppliers."
        })

    # Insight 3: Pricing Outliers
    df['abs_change'] = df['CY vs PY WAP USD (Fiscal)'].abs()
    outliers = df[df['abs_change'] > 5]
    for _, row in outliers.iterrows():
        actions.append({
            "type": "Flag Anomaly",
            "supplier": row["Supplier Name"],
            "item": row["Item Name"],
            "change": row["CY vs PY WAP USD (Fiscal)"],
            "action": f"The price for {row['Item Name']} from {row['Supplier Name']} has changed by ${row['CY vs PY WAP USD (Fiscal)']:.2f} per unit. Please investigate."
        })

    return actions
