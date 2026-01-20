📊 Sales Analytics System (Python)
📌 Project Overview

The Sales Analytics System is a Python-based application designed to process messy sales transaction data, enrich it with external API information, perform advanced analytics, and generate comprehensive business reports.

This project demonstrates practical skills in:

File handling & data cleaning

Data validation & filtering

Data analysis using lists and dictionaries

API integration

Report generation

Modular Python programming

Error handling and user interaction

📁 Project Structure
sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│   └── report_generator.py
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
└── output/
    └── sales_report.txt

🧩 Features Implemented
✅ Part 1: Data File Handling & Preprocessing

Handles non-UTF-8 encoded files

Cleans messy data (commas in numbers & text)

Removes invalid records based on business rules

Provides validation summary

✅ Part 2: Data Processing & Analytics

Total revenue calculation

Region-wise sales performance

Top selling products

Customer purchase analysis

Daily sales trends

Peak sales day

Low-performing products

✅ Part 3: API Integration

Fetches product data from DummyJSON API

Enriches sales data with:

Category

Brand

Rating

Saves enriched data to file

✅ Part 4: Report Generation

Generates a comprehensive text report including:

Overall summary

Region-wise performance

Top products & customers

Daily trends

Product performance analysis

API enrichment summary

✅ Part 5: Main Application

Interactive command-line execution

User-driven filtering (region & amount)

End-to-end workflow with progress indicators

Robust error handling

⚙️ Requirements
Python Version

Python 3.8 or higher

Python Libraries

Install dependencies using:

pip install -r requirements.txt


requirements.txt

requests

▶️ How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/ravishpandey007-debug/sales-analytics-system.git
cd sales-analytics-system

2️⃣ Ensure input file exists
data/sales_data.txt

3️⃣ Run the application
python main.py

📄 Output Files Generated
File	Description
data/enriched_sales_data.txt	Sales data enriched with API fields
output/sales_report.txt	Comprehensive analytics report
🧠 Business Value

This system helps stakeholders:

Identify high-performing regions and products

Understand customer behavior

Detect low-performing products

Make data-driven sales decisions

🏁 Conclusion

This project demonstrates a complete Python-based data analytics pipeline, combining real-world data cleaning, API enrichment, analytical insights, and professional reporting.