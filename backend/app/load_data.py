from pathlib import Path

import pandas as pd
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
)

from backend.app.database import engine


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

metadata = MetaData()


customers_table = Table(
    "customers",
    metadata,
    Column("customer_id", String(10), primary_key=True),
    Column("customer_name", String(150), nullable=False),
    Column("segment", String(50), nullable=False),
    Column("city", String(100), nullable=False),
    Column("state", String(2), nullable=False),
    Column("region", String(50), nullable=False),
)


products_table = Table(
    "products",
    metadata,
    Column("product_id", String(10), primary_key=True),
    Column("product_name", String(150), nullable=False),
    Column("category", String(100), nullable=False),
    Column("unit_price", Numeric(12, 2), nullable=False),
    Column("unit_cost", Numeric(12, 2), nullable=False),
)


orders_table = Table(
    "orders",
    metadata,
    Column("order_id", String(20), primary_key=True),
    Column(
        "customer_id",
        String(10),
        ForeignKey("customers.customer_id"),
        nullable=False,
    ),
    Column("order_date", Date, nullable=False),
    Column("sales_channel", String(50), nullable=False),
    Column("payment_method", String(50), nullable=False),
)


order_items_table = Table(
    "order_items",
    metadata,
    Column("order_item_id", String(20), primary_key=True),
    Column(
        "order_id",
        String(20),
        ForeignKey("orders.order_id"),
        nullable=False,
    ),
    Column(
        "product_id",
        String(10),
        ForeignKey("products.product_id"),
        nullable=False,
    ),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Numeric(12, 2), nullable=False),
    Column("discount_pct", Numeric(6, 4), nullable=False),
)


Index("idx_orders_customer_id", orders_table.c.customer_id)
Index("idx_orders_order_date", orders_table.c.order_date)
Index("idx_order_items_order_id", order_items_table.c.order_id)
Index("idx_order_items_product_id", order_items_table.c.product_id)


def load_csv_files():
    print("Lendo arquivos CSV...")

    customers = pd.read_csv(
        RAW_DATA_DIR / "customers.csv"
    )

    products = pd.read_csv(
        RAW_DATA_DIR / "products.csv"
    )

    orders = pd.read_csv(
        RAW_DATA_DIR / "orders.csv",
        parse_dates=["order_date"],
    )

    order_items = pd.read_csv(
        RAW_DATA_DIR / "order_items.csv"
    )

    return customers, products, orders, order_items


def create_database_tables():
    print("Criando tabelas no PostgreSQL...")

    metadata.drop_all(engine)
    metadata.create_all(engine)

    print("Tabelas criadas com sucesso!")


def insert_data(
    customers,
    products,
    orders,
    order_items,
):
    print("\nInserindo clientes...")

    customers.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
    )

    print(f"Clientes inseridos: {len(customers):,}")

    print("\nInserindo produtos...")

    products.to_sql(
        "products",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
    )

    print(f"Produtos inseridos: {len(products):,}")

    print("\nInserindo pedidos...")

    orders.to_sql(
        "orders",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
    )

    print(f"Pedidos inseridos: {len(orders):,}")

    print("\nInserindo itens dos pedidos...")

    order_items.to_sql(
        "order_items",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
    )

    print(
        f"Itens inseridos: {len(order_items):,}"
    )


def main():
    customers, products, orders, order_items = (
        load_csv_files()
    )

    create_database_tables()

    insert_data(
        customers,
        products,
        orders,
        order_items,
    )

    print("\n================================")
    print("Carga concluída com sucesso!")
    print("================================")


if __name__ == "__main__":
    main()