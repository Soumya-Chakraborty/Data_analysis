import pandas as pd
import numpy as np
from datetime import datetime

def prepare_data_for_powerbi_tableau():
    """
    Prepare cleaned data specifically formatted for Power BI and Tableau
    with all necessary calculated fields and proper data types
    """
    
    print("Loading and preparing data for Power BI/Tableau...")
    
    # Load the original data
    df = pd.read_excel('Online Retail Data Set (1).xlsx')
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Data cleaning - remove invalid records
    print("Applying data quality checks...")
    
    # Remove quantity less than 1 and unit price less than or equal to 0
    df_clean = df[(df['Quantity'] >= 1) & (df['UnitPrice'] > 0)].copy()
    
    print(f"Original records: {len(df)}")
    print(f"Clean records: {len(df_clean)}")
    print(f"Removed: {len(df) - len(df_clean)} records")
    
    # Calculate derived fields
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    # Date dimensions
    df_clean['Year'] = df_clean['InvoiceDate'].dt.year
    df_clean['Month'] = df_clean['InvoiceDate'].dt.month
    df_clean['MonthName'] = df_clean['InvoiceDate'].dt.month_name()
    df_clean['Quarter'] = df_clean['InvoiceDate'].dt.quarter
    df_clean['DayOfWeek'] = df_clean['InvoiceDate'].dt.day_name()
    df_clean['Date'] = df_clean['InvoiceDate'].dt.date
    df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M').astype(str)
    df_clean['WeekOfYear'] = df_clean['InvoiceDate'].dt.isocalendar().week
    
    # Customer analysis fields
    df_clean['HasCustomerID'] = df_clean['CustomerID'].notna()
    df_clean['CustomerID_Clean'] = df_clean['CustomerID'].fillna('Unknown')
    
    # Product categorization
    df_clean['StockCode_Category'] = df_clean['StockCode'].str.extract('([A-Za-z]+)')
    df_clean['StockCode_Category'] = df_clean['StockCode_Category'].fillna('Numeric')
    
    # Country grouping
    df_clean['IsUK'] = df_clean['Country'] == 'United Kingdom'
    df_clean['CountryGroup'] = df_clean['Country'].apply(lambda x: 'UK' if x == 'United Kingdom' else 'International')
    
    # Revenue categories
    df_clean['Revenue_Category'] = pd.cut(df_clean['Revenue'], 
                                         bins=[0, 10, 50, 200, float('inf')], 
                                         labels=['Low (£0-10)', 'Medium (£10-50)', 'High (£50-200)', 'Very High (£200+)'])
    
    # Quantity categories
    df_clean['Quantity_Category'] = pd.cut(df_clean['Quantity'], 
                                          bins=[0, 5, 20, 100, float('inf')], 
                                          labels=['Small (1-5)', 'Medium (6-20)', 'Large (21-100)', 'Bulk (100+)'])
    
    return df_clean

def create_question_specific_datasets(df_clean):
    """Create specific datasets for each question"""
    
    # Question 1: 2011 Monthly Revenue Data
    print("Creating Q1 dataset - 2011 Monthly Revenue...")
    df_2011 = df_clean[df_clean['Year'] == 2011].copy()
    
    # Monthly aggregation for Q1
    q1_monthly = df_2011.groupby(['Year', 'Month', 'MonthName', 'YearMonth']).agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique'
    }).reset_index()
    q1_monthly.columns = ['Year', 'Month', 'MonthName', 'YearMonth', 'Total_Revenue', 'Total_Quantity', 'Unique_Orders', 'Unique_Customers']
    q1_monthly.to_csv('Q1_2011_Monthly_Data.csv', index=False)
    
    # Question 2: Top Countries (excluding UK)
    print("Creating Q2 dataset - Top Countries...")
    df_no_uk = df_clean[df_clean['Country'] != 'United Kingdom'].copy()
    
    q2_countries = df_no_uk.groupby('Country').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique'
    }).reset_index()
    q2_countries.columns = ['Country', 'Total_Revenue', 'Total_Quantity', 'Unique_Orders', 'Unique_Customers']
    q2_countries = q2_countries.sort_values('Total_Revenue', ascending=False)
    q2_countries['Revenue_Rank'] = range(1, len(q2_countries) + 1)
    q2_countries.to_csv('Q2_Countries_Revenue_Analysis.csv', index=False)
    
    # Question 3: Customer Analysis
    print("Creating Q3 dataset - Customer Revenue...")
    df_customers = df_clean[df_clean['CustomerID'].notna()].copy()
    
    q3_customers = df_customers.groupby('CustomerID').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'InvoiceNo': 'nunique',
        'Country': 'first'
    }).reset_index()
    q3_customers.columns = ['CustomerID', 'Total_Revenue', 'Total_Quantity', 'Unique_Orders', 'Country']
    q3_customers = q3_customers.sort_values('Total_Revenue', ascending=False)
    q3_customers['Revenue_Rank'] = range(1, len(q3_customers) + 1)
    q3_customers['CustomerID'] = q3_customers['CustomerID'].astype(int)
    q3_customers.to_csv('Q3_Customer_Revenue_Analysis.csv', index=False)
    
    # Question 4: Country Demand Analysis (excluding UK)
    print("Creating Q4 dataset - Country Demand...")
    q4_demand = df_no_uk.groupby('Country').agg({
        'Quantity': 'sum',
        'Revenue': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique',
        'StockCode': 'nunique'
    }).reset_index()
    q4_demand.columns = ['Country', 'Total_Quantity_Demanded', 'Total_Revenue', 'Unique_Orders', 'Unique_Customers', 'Unique_Products']
    q4_demand = q4_demand.sort_values('Total_Quantity_Demanded', ascending=False)
    q4_demand['Demand_Rank'] = range(1, len(q4_demand) + 1)
    q4_demand['Avg_Order_Value'] = q4_demand['Total_Revenue'] / q4_demand['Unique_Orders']
    q4_demand['Avg_Quantity_Per_Order'] = q4_demand['Total_Quantity_Demanded'] / q4_demand['Unique_Orders']
    q4_demand.to_csv('Q4_Country_Demand_Analysis.csv', index=False)
    
    return q1_monthly, q2_countries, q3_customers, q4_demand

def create_data_dictionary():
    """Create a data dictionary for Power BI/Tableau users"""
    
    data_dict = {
        'Field_Name': [
            'InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 
            'CustomerID', 'Country', 'Revenue', 'Year', 'Month', 'MonthName', 'Quarter', 
            'DayOfWeek', 'Date', 'YearMonth', 'WeekOfYear', 'HasCustomerID', 'CustomerID_Clean',
            'StockCode_Category', 'IsUK', 'CountryGroup', 'Revenue_Category', 'Quantity_Category'
        ],
        'Data_Type': [
            'Text', 'Text', 'Text', 'Number', 'Date/Time', 'Currency', 'Number', 'Text',
            'Currency', 'Number', 'Number', 'Text', 'Number', 'Text', 'Date', 'Text', 'Number',
            'Boolean', 'Text', 'Text', 'Boolean', 'Text', 'Text', 'Text'
        ],
        'Description': [
            'Invoice number - unique identifier for each transaction',
            'Product stock code',
            'Product description',
            'Quantity of products purchased (cleaned: >= 1)',
            'Date and time of invoice',
            'Unit price per product (cleaned: > 0)',
            'Customer ID number',
            'Country where customer is located',
            'Calculated field: Quantity × UnitPrice',
            'Year extracted from InvoiceDate',
            'Month number (1-12) extracted from InvoiceDate',
            'Month name extracted from InvoiceDate',
            'Quarter (1-4) extracted from InvoiceDate',
            'Day of week name extracted from InvoiceDate',
            'Date only (without time) extracted from InvoiceDate',
            'Year-Month in YYYY-MM format',
            'Week number of the year',
            'Boolean: TRUE if CustomerID is not null',
            'CustomerID with nulls replaced by "Unknown"',
            'Category derived from StockCode letters',
            'Boolean: TRUE if Country is United Kingdom',
            'UK or International based on country',
            'Revenue grouped into categories',
            'Quantity grouped into categories'
        ],
        'Use_Case': [
            'Transaction identification, Order analysis',
            'Product analysis, Inventory tracking',
            'Product analysis, Text mining',
            'Sales volume analysis, Demand forecasting',
            'Time series analysis, Seasonality',
            'Pricing analysis, Revenue calculation',
            'Customer segmentation, Retention analysis',
            'Geographic analysis, Market expansion',
            'Revenue analysis, Profitability',
            'Annual trends, Year-over-year comparison',
            'Monthly trends, Seasonality',
            'Seasonal analysis, Month comparison',
            'Quarterly reporting, Business cycles',
            'Day-of-week patterns, Operational planning',
            'Daily analysis, Calendar visualization',
            'Monthly trending, Period comparison',
            'Weekly patterns, Short-term trends',
            'Customer data quality analysis',
            'Customer analysis including unknowns',
            'Product categorization, SKU analysis',
            'Domestic vs International analysis',
            'Market segmentation, Geographic focus',
            'Revenue segmentation, Value analysis',
            'Order size analysis, Bulk vs Retail'
        ]
    }
    
    dict_df = pd.DataFrame(data_dict)
    dict_df.to_csv('Data_Dictionary.csv', index=False)
    
    return dict_df

def main():
    """Main execution function"""
    print("=== POWER BI / TABLEAU DATA PREPARATION ===")
    print("Preparing cleaned datasets and documentation...")
    print("=" * 60)
    
    # Prepare main cleaned dataset
    df_clean = prepare_data_for_powerbi_tableau()
    
    # Save main cleaned dataset
    df_clean.to_csv('Master_Cleaned_Retail_Data.csv', index=False)
    print("Saved: Master_Cleaned_Retail_Data.csv")
    
    # Create question-specific datasets
    q1_data, q2_data, q3_data, q4_data = create_question_specific_datasets(df_clean)
    
    # Create data dictionary
    data_dict = create_data_dictionary()
    print("Saved: Data_Dictionary.csv")
    
    # Create summary report
    summary = f"""
DATA PREPARATION SUMMARY
========================

Total Records After Cleaning: {len(df_clean):,}
Date Range: {df_clean['InvoiceDate'].min()} to {df_clean['InvoiceDate'].max()}
Countries: {df_clean['Country'].nunique()}
Customers: {df_clean['CustomerID'].nunique()}
Products: {df_clean['StockCode'].nunique()}
Total Revenue: £{df_clean['Revenue'].sum():,.2f}

FILES CREATED FOR POWER BI/TABLEAU:
===================================

1. Master_Cleaned_Retail_Data.csv
   - Complete cleaned dataset with all derived fields
   - Use this for comprehensive analysis across all questions

2. Q1_2011_Monthly_Data.csv
   - Monthly aggregated data for 2011 revenue trend analysis
   - Supports Question 1: CEO's seasonal trend analysis

3. Q2_Countries_Revenue_Analysis.csv
   - Country-level revenue and quantity metrics (excluding UK)
   - Supports Question 2: CMO's top 10 countries analysis

4. Q3_Customer_Revenue_Analysis.csv
   - Customer-level revenue analysis with rankings
   - Supports Question 3: CMO's top customer identification

5. Q4_Country_Demand_Analysis.csv
   - Country demand metrics with expansion insights
   - Supports Question 4: CEO's market expansion analysis

6. Data_Dictionary.csv
   - Complete field definitions and use cases
   - Reference guide for all data fields

POWER BI IMPORT INSTRUCTIONS:
=============================
1. Open Power BI Desktop
2. Get Data > Text/CSV
3. Select the appropriate CSV file for your analysis
4. Use the data dictionary to understand field meanings
5. Create relationships between tables if using multiple datasets

TABLEAU IMPORT INSTRUCTIONS:
============================
1. Open Tableau Desktop
2. Connect > To a File > Text File
3. Select the appropriate CSV file
4. Use Data Interpreter if prompted
5. Check data types match the data dictionary specifications

DATA QUALITY NOTES:
===================
- Removed {len(pd.read_excel('Online Retail Data Set (1).xlsx')) - len(df_clean):,} records with invalid quantity (<1) or price (≤0)
- Missing CustomerIDs handled with 'Unknown' category
- All monetary values are in British Pounds (£)
- Revenue calculated as Quantity × UnitPrice after data cleaning
"""
    
    with open('Data_Preparation_Summary.txt', 'w') as f:
        f.write(summary)
    
    print("Saved: Data_Preparation_Summary.txt")
    print("\n" + "=" * 60)
    print("DATA PREPARATION COMPLETE!")
    print("\nGenerated Files:")
    print("- Master_Cleaned_Retail_Data.csv")
    print("- Q1_2011_Monthly_Data.csv")
    print("- Q2_Countries_Revenue_Analysis.csv") 
    print("- Q3_Customer_Revenue_Analysis.csv")
    print("- Q4_Country_Demand_Analysis.csv")
    print("- Data_Dictionary.csv")
    print("- Data_Preparation_Summary.txt")
    print("\nThese files are ready for import into Power BI or Tableau!")

if __name__ == "__main__":
    main()