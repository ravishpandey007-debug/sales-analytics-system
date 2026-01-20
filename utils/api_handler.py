import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        simplified_products = []
        for p in products:
            simplified_products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            })

        print(f"✅ Successfully fetched {len(simplified_products)} products from API")
        return simplified_products

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        pid = product.get("id")

        if pid is not None:
            product_mapping[pid] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

    return product_mapping
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        try:
            # Extract numeric ID from ProductID (P101 -> 101)
            numeric_id = int("".join(filter(str.isdigit, tx["ProductID"]))) % 100
            if numeric_id == 0:
                numeric_id = 100

            if numeric_id in product_mapping:
                api_data = product_mapping[numeric_id]

                enriched_tx["API_Category"] = api_data["category"]
                enriched_tx["API_Brand"] = api_data["brand"]
                enriched_tx["API_Rating"] = api_data["rating"]
                enriched_tx["API_Match"] = True
            else:
                enriched_tx["API_Category"] = None
                enriched_tx["API_Brand"] = None
                enriched_tx["API_Rating"] = None
                enriched_tx["API_Match"] = False

        except Exception:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    save_enriched_data(enriched_transactions)
    matched = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
    total = len(enriched_transactions)
    percentage = (matched / total * 100) if total else 0

    print(f"✓ Enriched {matched}/{total} transactions ({percentage:.1f}%)")

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(header)

            for tx in enriched_transactions:
                row = [
                    str(tx.get("TransactionID", "")),
                    str(tx.get("Date", "")),
                    str(tx.get("ProductID", "")),
                    str(tx.get("ProductName", "")),
                    str(tx.get("Quantity", "")),
                    str(tx.get("UnitPrice", "")),
                    str(tx.get("CustomerID", "")),
                    str(tx.get("Region", "")),
                    str(tx.get("API_Category", "")),
                    str(tx.get("API_Brand", "")),
                    str(tx.get("API_Rating", "")),
                    str(tx.get("API_Match", ""))
                ]

                file.write("|".join(row) + "\n")

        print(f"✅ Enriched data saved to {filename}")

    except IOError as e:
        print(f"❌ Failed to save enriched data: {e}")
