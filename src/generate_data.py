from pathlib import Path
import random

import numpy as np
import pandas as pd
from faker import Faker


# Configurações do projeto
SEED = 42

random.seed(SEED)
np.random.seed(SEED)
Faker.seed(SEED)

fake = Faker("pt_BR")


# Caminhos principais
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


print("Projeto configurado com sucesso!")
print(f"Pasta principal: {BASE_DIR}")
print(f"Pasta de dados: {RAW_DATA_DIR}")

PRODUCTS = [
    ["P001", "Notebook Pro 15", "Eletrônicos", 4599.90, 3400.00],
    ["P002", "Notebook Air 14", "Eletrônicos", 3499.90, 2600.00],
    ["P003", "Smartphone X", "Eletrônicos", 2899.90, 2100.00],
    ["P004", "Smartphone Lite", "Eletrônicos", 1599.90, 1150.00],
    ["P005", "Monitor 27", "Informática", 1299.90, 850.00],
    ["P006", "Monitor 24", "Informática", 899.90, 590.00],
    ["P007", "Teclado Mecânico", "Acessórios", 349.90, 190.00],
    ["P008", "Mouse Wireless", "Acessórios", 189.90, 95.00],
    ["P009", "Headset Gamer", "Acessórios", 299.90, 160.00],
    ["P010", "Webcam Full HD", "Acessórios", 249.90, 130.00],
    ["P011", "SSD 1TB", "Informática", 499.90, 290.00],
    ["P012", "SSD 500GB", "Informática", 299.90, 170.00],
    ["P013", "Cadeira Office", "Escritório", 1199.90, 720.00],
    ["P014", "Mesa Office", "Escritório", 899.90, 510.00],
    ["P015", "Hub USB-C", "Acessórios", 199.90, 90.00],
]

products_df = pd.DataFrame(
    PRODUCTS,
    columns=[
        "product_id",
        "product_name",
        "category",
        "unit_price",
        "unit_cost",
    ],
)

products_path = RAW_DATA_DIR / "products.csv"

products_df.to_csv(
    products_path,
    index=False,
    encoding="utf-8-sig",
)

print("\nTabela de produtos criada!")
print(products_df)
print(f"\nArquivo salvo em: {products_path}")

NUMBER_OF_CUSTOMERS = 15_000


def generate_customers(number_of_customers: int) -> pd.DataFrame:
    customers = []

    segments = [
        "Consumer",
        "Corporate",
        "Small Business",
    ]

    locations = [
        ("São Paulo", "SP", "Sudeste"),
        ("Sorocaba", "SP", "Sudeste"),
        ("Campinas", "SP", "Sudeste"),
        ("Rio de Janeiro", "RJ", "Sudeste"),
        ("Belo Horizonte", "MG", "Sudeste"),
        ("Curitiba", "PR", "Sul"),
        ("Porto Alegre", "RS", "Sul"),
        ("Florianópolis", "SC", "Sul"),
        ("Salvador", "BA", "Nordeste"),
        ("Recife", "PE", "Nordeste"),
        ("Fortaleza", "CE", "Nordeste"),
        ("Brasília", "DF", "Centro-Oeste"),
        ("Goiânia", "GO", "Centro-Oeste"),
    ]

    for i in range(1, number_of_customers + 1):
        city, state, region = random.choice(locations)

        customer = {
            "customer_id": f"C{i:05d}",
            "customer_name": fake.name(),
            "segment": random.choice(segments),
            "city": city,
            "state": state,
            "region": region,
        }

        customers.append(customer)

    return pd.DataFrame(customers)

customers_df = generate_customers(NUMBER_OF_CUSTOMERS)

customers_path = RAW_DATA_DIR / "customers.csv"

customers_df.to_csv(
    customers_path,
    index=False,
    encoding="utf-8-sig",
)

print("\nTabela de clientes criada!")
print(customers_df.head(10))
print(f"\nTotal de clientes: {len(customers_df):,}")
print(f"Arquivo salvo em: {customers_path}")

from datetime import datetime, timedelta

NUMBER_OF_ORDERS = 100_000


def random_date(start_date: datetime, end_date: datetime) -> datetime:
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    return start_date + timedelta(days=random_days)


def generate_orders(
    number_of_orders: int,
    customers: pd.DataFrame,
) -> pd.DataFrame:

    orders = []

    channels = [
        "Website",
        "App",
        "Marketplace",
        "Loja Física",
    ]

    payment_methods = [
        "PIX",
        "Cartão de Crédito",
        "Cartão de Débito",
        "Boleto",
    ]

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)

    customer_ids = customers["customer_id"].tolist()

    for i in range(1, number_of_orders + 1):

        order = {
            "order_id": f"O{i:07d}",
            "customer_id": random.choice(customer_ids),
            "order_date": random_date(start_date, end_date),
            "sales_channel": random.choice(channels),
            "payment_method": random.choice(payment_methods),
        }

        orders.append(order)

    return pd.DataFrame(orders)


orders_df = generate_orders(
    NUMBER_OF_ORDERS,
    customers_df,
)

orders_path = RAW_DATA_DIR / "orders.csv"

orders_df.to_csv(
    orders_path,
    index=False,
    encoding="utf-8-sig",
)

print("\nTabela de pedidos criada!")
print(orders_df.head(10))
print(f"\nTotal de pedidos: {len(orders_df):,}")
print(f"Arquivo salvo em: {orders_path}")

def generate_order_items(
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:

    order_items = []

    product_records = products.to_dict("records")

    item_counter = 1

    for order_id in orders["order_id"]:

        # Cada pedido terá entre 1 e 4 produtos
        number_of_items = random.randint(1, 4)

        selected_products = random.sample(
            product_records,
            k=number_of_items,
        )

        for product in selected_products:

            quantity = random.randint(1, 5)

            discount = random.choices(
                [0.00, 0.05, 0.10, 0.15, 0.20],
                weights=[50, 20, 15, 10, 5],
                k=1,
            )[0]

            order_item = {
                "order_item_id": f"OI{item_counter:07d}",
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": product["unit_price"],
                "discount_pct": discount,
            }

            order_items.append(order_item)

            item_counter += 1

    return pd.DataFrame(order_items)


order_items_df = generate_order_items(
    orders_df,
    products_df,
)

order_items_path = RAW_DATA_DIR / "order_items.csv"

order_items_df.to_csv(
    order_items_path,
    index=False,
    encoding="utf-8-sig",
)

print("\nTabela de itens dos pedidos criada!")
print(order_items_df.head(10))

print(f"\nTotal de itens vendidos: {len(order_items_df):,}")
print(f"Arquivo salvo em: {order_items_path}")