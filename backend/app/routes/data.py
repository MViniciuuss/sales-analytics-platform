from fastapi import APIRouter, Query
from sqlalchemy import text

from backend.app.database import engine


router = APIRouter(
    prefix="/api",
    tags=["Data"],
)


@router.get("/customers")
def get_customers(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = text(
        """
        SELECT
            customer_id,
            customer_name,
            segment,
            city,
            state,
            region
        FROM customers
        ORDER BY customer_id
        LIMIT :limit
        OFFSET :offset
        """
    )

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            {
                "limit": limit,
                "offset": offset,
            },
        ).mappings().all()

    return {
        "data": [dict(row) for row in rows],
        "limit": limit,
        "offset": offset,
    }


@router.get("/products")
def get_products():
    query = text(
        """
        SELECT
            product_id,
            product_name,
            category,
            unit_price,
            unit_cost
        FROM products
        ORDER BY product_id
        """
    )

    with engine.connect() as connection:
        rows = connection.execute(
            query
        ).mappings().all()

    return {
        "data": [dict(row) for row in rows]
    }


@router.get("/orders")
def get_orders(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = text(
        """
        SELECT
            o.order_id,
            o.order_date,
            o.sales_channel,
            o.payment_method,
            c.customer_id,
            c.customer_name,
            c.city,
            c.state
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
        LIMIT :limit
        OFFSET :offset
        """
    )

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            {
                "limit": limit,
                "offset": offset,
            },
        ).mappings().all()

    return {
        "data": [dict(row) for row in rows],
        "limit": limit,
        "offset": offset,
    }