from datetime import datetime
from collections import defaultdict

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # =============================
    # BASIC METRICS
    # =============================
    total_transactions = len(transactions)
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx["Date"] for tx in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =============================
    # ANALYTICS
    # =============================
    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day, peak_revenue, peak_txn_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # Avg transaction value per region
    region_avg_value = {}
    for region, data in region_stats.items():
        region_avg_value[region] = data["total_sales"] / data["transaction_count"]

    # =============================
    # API ENRICHMENT SUMMARY
    # =============================
    enriched_success = [tx for tx in enriched_transactions if tx.get("API_Match")]
    enriched_failed = [tx for tx in enriched_transactions if not tx.get("API_Match")]

    success_rate = (
        (len(enriched_success) / len(enriched_transactions)) * 100
        if enriched_transactions else 0
    )

    failed_products = sorted(
        set(tx["ProductName"] for tx in enriched_failed)
    )

    # =============================
    # WRITE REPORT
    # =============================
    with open(output_file, "w", encoding="utf-8") as f:

        # 1. HEADER
        f.write("=" * 60 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {now}\n")
        f.write(f"     Records Processed: {total_transactions}\n")
        f.write("=" * 60 + "\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>15}{'Transactions':>15}\n")

        for region, data in region_stats.items():
            f.write(
                f"{region:<10}"
                f"₹{data['total_sales']:>14,.2f}"
                f"{data['percentage']:>14.2f}%"
                f"{data['transaction_count']:>15}\n"
            )
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<6}{'Product Name':<25}{'Qty Sold':>10}{'Revenue':>15}\n")

        for idx, (name, qty, rev) in enumerate(top_products, start=1):
            f.write(f"{idx:<6}{name:<25}{qty:>10}₹{rev:>14,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<6}{'Customer ID':<15}{'Total Spent':>15}{'Orders':>10}\n")

        for idx, (cid, data) in enumerate(list(customers.items())[:5], start=1):
            f.write(
                f"{idx:<6}{cid:<15}"
                f"₹{data['total_spent']:>14,.2f}"
                f"{data['purchase_count']:>10}\n"
            )
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Transactions':>15}{'Customers':>15}\n")

        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}"
                f"₹{data['revenue']:>14,.2f}"
                f"{data['transaction_count']:>15}"
                f"{data['unique_customers']:>15}\n"
            )
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 60 + "\n")
        f.write(f"Best Selling Day: {peak_day} (₹{peak_revenue:,.2f}, {peak_txn_count} transactions)\n\n")

        f.write("Low Performing Products:\n")
        if low_products:
            for name, qty, rev in low_products:
                f.write(f" - {name}: Qty={qty}, Revenue=₹{rev:,.2f}\n")
        else:
            f.write(" - None\n")

        f.write("\nAverage Transaction Value per Region:\n")
        for region, value in region_avg_value.items():
            f.write(f" - {region}: ₹{value:,.2f}\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Transactions Enriched: {len(enriched_transactions)}\n")
        f.write(f"Successful Enrichments:      {len(enriched_success)}\n")
        f.write(f"Success Rate:                {success_rate:.2f}%\n\n")

        f.write("Products Not Enriched:\n")
        if failed_products:
            for p in failed_products:
                f.write(f" - {p}\n")
        else:
            f.write(" - None\n")

    print(f"✅ Sales report generated successfully at: {output_file}")
