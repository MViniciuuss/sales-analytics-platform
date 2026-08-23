from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]

SALES_DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_analytics.csv"
)


def get_dashboard_summary():
    """Calcula os principais KPIs da plataforma."""

    sales = pd.read_csv(SALES_DATA_PATH)

    total_revenue = sales["net_revenue"].sum()
    total_profit = sales["profit"].sum()

    total_orders = sales["order_id"].nunique()
    total_customers = sales["customer_id"].nunique()

    total_items = sales["quantity"].sum()

    average_ticket = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    profit_margin = (
        (total_profit / total_revenue) * 100
        if total_revenue > 0
        else 0
    )

    return {
        "total_revenue": round(float(total_revenue), 2),
        "total_profit": round(float(total_profit), 2),
        "profit_margin": round(float(profit_margin), 2),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "total_items": int(total_items),
        "average_ticket": round(float(average_ticket), 2),
    }