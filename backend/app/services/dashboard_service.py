from sqlalchemy import text

from backend.app.database import engine


def get_dashboard_summary():
    """Calcula os principais KPIs diretamente no PostgreSQL."""

    query = text(
        """
        SELECT
            ROUND(
                SUM(
                    oi.quantity
                    * oi.unit_price
                    * (1 - oi.discount_pct)
                ),
                2
            ) AS total_revenue,

            ROUND(
                SUM(
                    (
                        oi.quantity
                        * oi.unit_price
                        * (1 - oi.discount_pct)
                    )
                    -
                    (
                        oi.quantity
                        * p.unit_cost
                    )
                ),
                2
            ) AS total_profit,

            COUNT(DISTINCT o.order_id) AS total_orders,

            COUNT(DISTINCT o.customer_id) AS total_customers,

            SUM(oi.quantity) AS total_items

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query).mappings().one()

    total_revenue = float(result["total_revenue"] or 0)
    total_profit = float(result["total_profit"] or 0)
    total_orders = int(result["total_orders"] or 0)
    total_customers = int(result["total_customers"] or 0)
    total_items = int(result["total_items"] or 0)

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
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "profit_margin": round(profit_margin, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_items": total_items,
        "average_ticket": round(average_ticket, 2),
        "data_source": "PostgreSQL",
    }