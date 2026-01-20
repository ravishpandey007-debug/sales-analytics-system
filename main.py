from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
)
from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # -------------------------------------------------
        # 1. Read sales data
        # -------------------------------------------------
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # -------------------------------------------------
        # 2. Parse and clean
        # -------------------------------------------------
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # -------------------------------------------------
        # 3. Display filter options
        # -------------------------------------------------
        regions = sorted(set(tx["Region"] for tx in parsed_transactions if tx.get("Region")))
        amounts = [
            tx["Quantity"] * tx["UnitPrice"]
            for tx in parsed_transactions
            if tx["Quantity"] > 0 and tx["UnitPrice"] > 0
        ]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        if amounts:
            print(f"Amount Range: ₹{int(min(amounts)):,} - ₹{int(max(amounts)):,}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if apply_filter == "y":
            region_filter = input("Enter region (or press Enter to skip): ").strip()
            region_filter = region_filter if region_filter else None

            min_val = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_val = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_val) if min_val else None
            max_amount = float(max_val) if max_val else None

        # -------------------------------------------------
        # 4. Validate and filter
        # -------------------------------------------------
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            parsed_transactions,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )

        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # -------------------------------------------------
        # 5. Analysis
        # -------------------------------------------------
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # -------------------------------------------------
        # 6. Fetch API data
        # -------------------------------------------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # -------------------------------------------------
        # 7. Enrich data
        # -------------------------------------------------
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        success_count = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
        success_rate = (success_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

        print(f"✓ Enriched {success_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")

        # -------------------------------------------------
        # 8. Save enriched data (already done inside function)
        # -------------------------------------------------
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # -------------------------------------------------
        # 9. Generate report
        # -------------------------------------------------
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # -------------------------------------------------
        # 10. Done
        # -------------------------------------------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An unexpected error occurred.")
        print("Details:", str(e))
        print("Please check your data and try again.")


if __name__ == "__main__":
    main()
