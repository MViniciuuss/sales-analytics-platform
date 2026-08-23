from pathlib import Path

import pandas as pd


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# EXTRACT
# ============================================================

def load_raw_data():
    """Carrega os arquivos CSV da camada raw."""

    print("Carregando dados brutos...")

    customers = pd.read_csv(
        RAW_DATA_DIR / "customers.csv"
    )

    products = pd.read_csv(
        RAW_DATA_DIR / "products.csv"
    )

    orders = pd.read_csv(
        RAW_DATA_DIR / "orders.csv"
    )

    order_items = pd.read_csv(
        RAW_DATA_DIR / "order_items.csv"
    )

    return customers, products, orders, order_items


# ============================================================
# RESUMO DOS DADOS
# ============================================================

def show_dataset_summary(
    customers,
    products,
    orders,
    order_items,
):
    """Exibe um resumo inicial das bases."""

    print("\n===== RESUMO DOS DADOS =====")

    print(f"Clientes: {len(customers):,}")
    print(f"Produtos: {len(products):,}")
    print(f"Pedidos: {len(orders):,}")
    print(f"Itens de pedidos: {len(order_items):,}")

    print("\n============================")


# ============================================================
# DATA QUALITY
# ============================================================

def validate_data_quality(
    customers,
    products,
    orders,
    order_items,
):
    """Executa validações básicas de qualidade dos dados."""

    print("\n===== DATA QUALITY =====")

    datasets = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
    }

    # Valores nulos
    print("\nValores nulos:")

    for name, dataframe in datasets.items():
        null_values = dataframe.isnull().sum().sum()
        print(f"{name}: {null_values}")

    # Linhas duplicadas
    print("\nLinhas duplicadas:")

    for name, dataframe in datasets.items():
        duplicated_rows = dataframe.duplicated().sum()
        print(f"{name}: {duplicated_rows}")

    # IDs duplicados
    duplicated_customer_ids = (
        customers["customer_id"].duplicated().sum()
    )

    duplicated_product_ids = (
        products["product_id"].duplicated().sum()
    )

    duplicated_order_ids = (
        orders["order_id"].duplicated().sum()
    )

    duplicated_order_item_ids = (
        order_items["order_item_id"].duplicated().sum()
    )

    print("\nIDs duplicados:")
    print(f"customer_id: {duplicated_customer_ids}")
    print(f"product_id: {duplicated_product_ids}")
    print(f"order_id: {duplicated_order_ids}")
    print(f"order_item_id: {duplicated_order_item_ids}")

    # Relacionamentos
    invalid_customer_orders = (
        ~orders["customer_id"].isin(
            customers["customer_id"]
        )
    ).sum()

    invalid_order_items = (
        ~order_items["order_id"].isin(
            orders["order_id"]
        )
    ).sum()

    invalid_products = (
        ~order_items["product_id"].isin(
            products["product_id"]
        )
    ).sum()

    print("\nRelacionamentos inválidos:")
    print(
        f"Pedidos sem cliente válido: "
        f"{invalid_customer_orders}"
    )
    print(
        f"Itens sem pedido válido: "
        f"{invalid_order_items}"
    )
    print(
        f"Itens sem produto válido: "
        f"{invalid_products}"
    )

    print("\n========================")


# ============================================================
# TRANSFORM
# ============================================================

def transform_sales_data(
    customers,
    products,
    orders,
    order_items,
):
    """Integra tabelas e cria métricas analíticas."""

    print("\nTransformando dados...")

    # Itens de pedidos + pedidos
    sales = order_items.merge(
        orders,
        on="order_id",
        how="left",
        validate="many_to_one",
    )

    # Produtos
    sales = sales.merge(
        products[
            [
                "product_id",
                "product_name",
                "category",
                "unit_cost",
            ]
        ],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    # Clientes
    sales = sales.merge(
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    # Data
    sales["order_date"] = pd.to_datetime(
        sales["order_date"]
    )

    # Receita bruta
    sales["gross_revenue"] = (
        sales["quantity"]
        * sales["unit_price"]
    )

    # Valor do desconto
    sales["discount_amount"] = (
        sales["gross_revenue"]
        * sales["discount_pct"]
    )

    # Receita líquida
    sales["net_revenue"] = (
        sales["gross_revenue"]
        - sales["discount_amount"]
    )

    # Custo total
    sales["total_cost"] = (
        sales["quantity"]
        * sales["unit_cost"]
    )

    # Lucro
    sales["profit"] = (
        sales["net_revenue"]
        - sales["total_cost"]
    )

    # Margem de lucro
    sales["profit_margin"] = (
        sales["profit"]
        / sales["net_revenue"]
    )

    # Dimensões temporais
    sales["year"] = (
        sales["order_date"].dt.year
    )

    sales["month"] = (
        sales["order_date"].dt.month
    )

    sales["year_month"] = (
        sales["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Arredondamento financeiro
    financial_columns = [
        "gross_revenue",
        "discount_amount",
        "net_revenue",
        "total_cost",
        "profit",
        "profit_margin",
    ]

    sales[financial_columns] = (
        sales[financial_columns]
        .round(2)
    )

    print("Transformação concluída!")
    print(f"Linhas finais: {len(sales):,}")
    print(f"Colunas finais: {len(sales.columns)}")

    return sales


# ============================================================
# MAIN
# ============================================================

def main():

    customers, products, orders, order_items = (
        load_raw_data()
    )

    show_dataset_summary(
        customers,
        products,
        orders,
        order_items,
    )

    validate_data_quality(
        customers,
        products,
        orders,
        order_items,
    )

    sales = transform_sales_data(
        customers,
        products,
        orders,
        order_items,
    )

    output_path = (
        PROCESSED_DATA_DIR
        / "sales_analytics.csv"
    )

    sales.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nDataset analítico criado!")
    print(f"Arquivo: {output_path}")

    print("\nPrimeiras linhas:")
    print(sales.head())


if __name__ == "__main__":
    main()