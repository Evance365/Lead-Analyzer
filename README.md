Lead Analyzer

Lead Analyzer is a Python CLI tool for importing, cleaning, analyzing, and visualizing lead or customer data from CSV files. It is designed to help sales, marketing, and operations teams gain actionable insights from raw lead datasets.

Features

CSV Import: Load leads or customer data using Pandas.

Data Cleaning: Handle missing values, standardize text fields, validate emails, and ensure numeric fields are consistent.

Lead Analysis:

Calculate overall conversion rate

Performance analysis by lead source

Breakdown by lead status

Daily and weekly trend analysis

Visualizations:

Charts for lead sources, lead status, daily trends, and lead value

Export Reports: Save cleaned data and analysis reports as CSV or Excel files.

Command-Line Interface: Simple menu for easy navigation.

Installation

Clone the repository:

git clone https://github.com/Evance365/lead-analyzer.git
cd lead-analyzer


Set up a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux / macOS


Install dependencies:

pip install -r requirements.txt

Usage

Run the application:

python src/main.py


The menu allows you to:

Load CSV file

Clean data

Calculate conversion rate

Analyze by source

Analyze by status

Analyze trends (daily/weekly)

Create visualizations

Export report (CSV / Excel)

Show data information

Exit

Example Workflow

Load your CSV of leads.

Clean the dataset to handle missing or invalid values.

Calculate overall conversion rate.

Analyze leads by source and status.

Explore daily and weekly trends.

Generate charts to visualize performance.

Export reports to CSV or Excel for stakeholders.

Project Structure
lead-analyzer/
│
├── src/
│   ├── lead_analyzer.py   # Core analysis class
│   └── main.py            # CLI entry point
│
├── data/
│   └── sample_leads.csv   # Sample data file
│
├── README.md
├── .gitignore
└── requirements.txt

License

MIT License. You are free to use, modify, and distribute this project.

Contact

Created by Evance Odhiambo
GitHub: https://github.com/Evance365
