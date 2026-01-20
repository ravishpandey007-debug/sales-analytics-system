# =========================================================
# TASK 1.2: Parse and Clean Data
# =========================================================

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            transaction = {
                "TransactionID": parts[0].strip(),
                "Date": parts[1].strip(),
                "ProductID": parts[2].strip(),
                "ProductName": parts[3].replace(",", "").strip(),
                "Quantity": int(parts[4].replace(",", "").strip()),
                "UnitPrice": float(parts[5].replace(",", "").strip()),
                "CustomerID": parts[6].strip(),
                "Region": parts[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows with conversion issues
            continue

    return transactions


# =========================================================
# TASK 1.3: Data Validation and Filtering
# =========================================================

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid_transactions = []
    invalid_count = 0
    total_input = len(transactions)

    for tx in transactions:
        try:
            if (
                tx["Quantity"] <= 0 or
                tx["UnitPrice"] <= 0 or
                not tx["CustomerID"] or
                not tx["Region"] or
                not tx["TransactionID"].startswith("T") or
                not tx["ProductID"].startswith("P") or
                not tx["CustomerID"].startswith("C")
            ):
                invalid_count += 1
                continue

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    # Display available regions
    regions = sorted(set(tx["Region"] for tx in valid_transactions))
    print("📍 Available Regions:", regions)

    # Display transaction amount range
    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid_transactions]
    if amounts:
        print(f"💰 Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    filtered_by_region = 0
    filtered_by_amount = 0

    # Filter by region
    if region:
        before = len(valid_transactions)
        valid_transactions = [tx for tx in valid_transactions if tx["Region"] == region]
        filtered_by_region = before - len(valid_transactions)
        print(f"🔎 Records after region filter ({region}): {len(valid_transactions)}")

    # Filter by transaction amount
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)

        def amount_valid(tx):
            amount = tx["Quantity"] * tx["UnitPrice"]
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True

        valid_transactions = [tx for tx in valid_transactions if amount_valid(tx)]
        filtered_by_amount = before - len(valid_transactions)
        print(f"🔎 Records after amount filter: {len(valid_transactions)}")

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
    return valid_transactions, invalid_count, summary


# =========================================================
# TASK 2.1(a): Total Revenue
# =========================================================

def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return round(total, 2)


# =========================================================
# TASK 2.1(b): Region-wise Sales Analysis
# =========================================================

def region_wise_sales(transactions):
    region_data = {}
    grand_total = 0.0

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {"total_sales": 0.0, "transaction_count": 0}

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1
        grand_total += revenue

    result = {}
    for region, data in region_data.items():
        percentage = (data["total_sales"] / grand_total) * 100 if grand_total else 0
        result[region] = {
            "total_sales": round(data["total_sales"], 2),
            "transaction_count": data["transaction_count"],
            "percentage": round(percentage, 2)
        }

    # Sort by total_sales descending
    return dict(sorted(result.items(), key=lambda x: x[1]["total_sales"], reverse=True))


# =========================================================
# TASK 2.1(c): Top Selling Products
# =========================================================

def top_selling_products(transactions, n=5):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {"quantity": 0, "revenue": 0.0}

        products[name]["quantity"] += qty
        products[name]["revenue"] += revenue

    result = [(name, data["quantity"], round(data["revenue"], 2))
              for name, data in products.items()]

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


# =========================================================
# TASK 2.1(d): Customer Purchase Analysis
# =========================================================

def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(tx["ProductName"])

    result = {}
    for cid, data in customers.items():
        avg = data["total_spent"] / data["purchase_count"]
        result[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg, 2),
            "products_bought": sorted(list(data["products_bought"]))
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True))


# =========================================================
# TASK 2.2(a): Daily Sales Trend
# =========================================================

def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += revenue
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(tx["CustomerID"])

    result = {}
    for date in sorted(daily.keys()):
        result[date] = {
            "revenue": round(daily[date]["revenue"], 2),
            "transaction_count": daily[date]["transaction_count"],
            "unique_customers": len(daily[date]["customers"])
        }

    return result


# =========================================================
# TASK 2.2(b): Peak Sales Day
# =========================================================

def find_peak_sales_day(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily:
            daily[date] = {"revenue": 0.0, "count": 0}

        daily[date]["revenue"] += revenue
        daily[date]["count"] += 1

    peak_date = max(daily, key=lambda d: daily[d]["revenue"])
    return (peak_date, round(daily[peak_date]["revenue"], 2), daily[peak_date]["count"])


# =========================================================
# TASK 2.3(a): Low Performing Products
# =========================================================

def low_performing_products(transactions, threshold=10):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {"quantity": 0, "revenue": 0.0}

        products[name]["quantity"] += qty
        products[name]["revenue"] += revenue

    result = [(name, data["quantity"], round(data["revenue"], 2))
              for name, data in products.items()
              if data["quantity"] < threshold]

    result.sort(key=lambda x: x[1])
    return result
