import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend for headless environments
import matplotlib
matplotlib.use('Agg')

# Set style for better visualizations
try:
    plt.style.use('seaborn-v0_8')
except:
    try:
        plt.style.use('seaborn')
    except:
        plt.style.use('default')

sns.set_palette("husl")

def load_and_clean_data():
    """Load and clean the retail data according to specifications"""
    print("Loading data...")
    df = pd.read_csv('online_retail_data.csv')
    
    print(f"Original data shape: {df.shape}")
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Data cleaning as per requirements
    print("Cleaning data...")
    
    # Remove records with quantity less than 1
    df_clean = df[df['Quantity'] >= 1].copy()
    print(f"Removed {len(df) - len(df_clean)} records with quantity < 1")
    
    # Remove records with unit price less than or equal to 0
    df_clean = df_clean[df_clean['UnitPrice'] > 0].copy()
    print(f"Final cleaned data shape: {df_clean.shape}")
    
    # Calculate revenue
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    # Extract date components
    df_clean['Year'] = df_clean['InvoiceDate'].dt.year
    df_clean['Month'] = df_clean['InvoiceDate'].dt.month
    df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')
    
    return df_clean

def question_1_time_series_2011(df):
    """Q1: Time series of revenue data for 2011 by month"""
    print("\n=== Question 1: 2011 Monthly Revenue Time Series ===")
    
    # Filter for 2011 data only
    df_2011 = df[df['Year'] == 2011].copy()
    
    # Group by month and calculate total revenue
    monthly_revenue = df_2011.groupby('YearMonth')['Revenue'].sum().reset_index()
    monthly_revenue['Month_Date'] = monthly_revenue['YearMonth'].dt.to_timestamp()
    
    # Create the visualization
    plt.figure(figsize=(14, 8))
    plt.plot(monthly_revenue['Month_Date'], monthly_revenue['Revenue'], 
             marker='o', linewidth=3, markersize=8, color='#2E86AB')
    
    plt.title('Monthly Revenue Trend for 2011\nSeasonal Analysis for CEO Forecasting', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Revenue (£)', fontsize=12, fontweight='bold')
    
    # Format y-axis to show values in millions
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x/1e6:.1f}M'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Highlight seasonal trends with annotations
    max_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmax()]
    min_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmin()]
    
    plt.annotate(f'Peak: {max_month["YearMonth"]}\n£{max_month["Revenue"]/1e6:.1f}M', 
                xy=(max_month['Month_Date'], max_month['Revenue']),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    plt.savefig('Q1_2011_Monthly_Revenue_Trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return monthly_revenue

def question_2_top_countries(df):
    """Q2: Top 10 countries by revenue (excluding UK) with quantity"""
    print("\n=== Question 2: Top 10 Countries by Revenue (Excluding UK) ===")
    
    # Exclude United Kingdom
    df_no_uk = df[df['Country'] != 'United Kingdom'].copy()
    
    # Group by country and calculate metrics
    country_metrics = df_no_uk.groupby('Country').agg({
        'Revenue': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    # Get top 10 countries by revenue
    top_10_countries = country_metrics.nlargest(10, 'Revenue')
    
    # Create dual-axis visualization
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Revenue bars
    bars = ax1.bar(range(len(top_10_countries)), top_10_countries['Revenue'], 
                   color='#A23B72', alpha=0.7, label='Revenue')
    ax1.set_xlabel('Country', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Revenue (£)', fontsize=12, fontweight='bold', color='#A23B72')
    ax1.tick_params(axis='y', labelcolor='#A23B72')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x/1e6:.1f}M'))
    
    # Quantity line on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(range(len(top_10_countries)), top_10_countries['Quantity'], 
                    color='#F18F01', marker='o', linewidth=3, markersize=8, label='Quantity')
    ax2.set_ylabel('Quantity Sold', fontsize=12, fontweight='bold', color='#F18F01')
    ax2.tick_params(axis='y', labelcolor='#F18F01')
    
    # Set x-axis labels
    ax1.set_xticks(range(len(top_10_countries)))
    ax1.set_xticklabels(top_10_countries['Country'], rotation=45, ha='right')
    
    plt.title('Top 10 Countries by Revenue and Quantity Sold\n(Excluding United Kingdom)', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('Q2_Top_10_Countries_Revenue_Quantity.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return top_10_countries

def question_3_top_customers(df):
    """Q3: Top 10 customers by revenue"""
    print("\n=== Question 3: Top 10 Customers by Revenue ===")
    
    # Remove rows with missing CustomerID
    df_customers = df[df['CustomerID'].notna()].copy()
    
    # Group by customer and calculate total revenue
    customer_revenue = df_customers.groupby('CustomerID')['Revenue'].sum().reset_index()
    
    # Get top 10 customers
    top_10_customers = customer_revenue.nlargest(10, 'Revenue')
    top_10_customers['CustomerID'] = top_10_customers['CustomerID'].astype(int)
    top_10_customers = top_10_customers.sort_values('Revenue', ascending=True)  # For horizontal bar chart
    
    # Create horizontal bar chart
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top_10_customers)), top_10_customers['Revenue'], 
                    color=sns.color_palette("viridis", len(top_10_customers)))
    
    # Customize the chart
    plt.xlabel('Revenue (£)', fontsize=12, fontweight='bold')
    plt.ylabel('Customer ID', fontsize=12, fontweight='bold')
    plt.title('Top 10 Revenue Generating Customers\n(Highest to Lowest Revenue)', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Set y-axis labels
    plt.yticks(range(len(top_10_customers)), 
               [f'Customer {int(cid)}' for cid in top_10_customers['CustomerID']])
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x/1e3:.0f}K'))
    
    # Add value labels on bars
    for i, (idx, row) in enumerate(top_10_customers.iterrows()):
        plt.text(row['Revenue'] + 1000, i, f'£{row["Revenue"]/1e3:.0f}K', 
                va='center', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('Q3_Top_10_Customers_Revenue.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return top_10_customers

def question_4_demand_by_country(df):
    """Q4: Demand analysis by country (excluding UK)"""
    print("\n=== Question 4: Product Demand by Country (Excluding UK) ===")
    
    # Exclude United Kingdom
    df_no_uk = df[df['Country'] != 'United Kingdom'].copy()
    
    # Calculate demand metrics by country
    country_demand = df_no_uk.groupby('Country').agg({
        'Quantity': 'sum',
        'Revenue': 'sum',
        'InvoiceNo': 'nunique'  # Number of unique orders
    }).reset_index()
    
    country_demand.columns = ['Country', 'Total_Quantity', 'Total_Revenue', 'Unique_Orders']
    
    # Create a comprehensive bubble chart
    plt.figure(figsize=(16, 10))
    
    # Use quantity for y-axis, revenue for x-axis, and orders for bubble size
    scatter = plt.scatter(country_demand['Total_Revenue'], 
                         country_demand['Total_Quantity'],
                         s=country_demand['Unique_Orders']/10,  # Scale bubble size
                         alpha=0.7,
                         c=range(len(country_demand)),
                         cmap='tab20')
    
    # Add country labels
    for i, row in country_demand.iterrows():
        plt.annotate(row['Country'], 
                    (row['Total_Revenue'], row['Total_Quantity']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=9, fontweight='bold')
    
    plt.xlabel('Total Revenue (£)', fontsize=12, fontweight='bold')
    plt.ylabel('Total Quantity Demanded', fontsize=12, fontweight='bold')
    plt.title('Product Demand Analysis by Country\n(Bubble size represents number of unique orders)\nExcluding United Kingdom', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Format axes
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x/1e6:.1f}M'))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('Q4_Country_Demand_Analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Also create a summary table
    country_demand_sorted = country_demand.sort_values('Total_Quantity', ascending=False)
    
    print("\nTop 15 Countries by Demand (Total Quantity):")
    print(country_demand_sorted.head(15)[['Country', 'Total_Quantity', 'Total_Revenue', 'Unique_Orders']])
    
    return country_demand_sorted

def export_cleaned_data(df):
    """Export cleaned data for Tableau/Power BI"""
    print("\n=== Exporting Cleaned Data ===")
    
    # Export full cleaned dataset
    df.to_csv('cleaned_retail_data.csv', index=False)
    print("Exported: cleaned_retail_data.csv")
    
    # Export 2011 data specifically for Question 1
    df_2011 = df[df['Year'] == 2011]
    df_2011.to_csv('cleaned_retail_data_2011.csv', index=False)
    print("Exported: cleaned_retail_data_2011.csv")
    
    # Create summary statistics
    summary_stats = {
        'Total Records': len(df),
        'Date Range': f"{df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}",
        'Total Revenue': df['Revenue'].sum(),
        'Unique Countries': df['Country'].nunique(),
        'Unique Customers': df['CustomerID'].nunique(),
        'Unique Products': df['StockCode'].nunique()
    }
    
    print("\nData Summary:")
    for key, value in summary_stats.items():
        print(f"{key}: {value}")

def main():
    """Main execution function"""
    print("=== RETAIL DATA ANALYSIS ===")
    print("Creating visualizations for CEO and CMO questions")
    print("=" * 50)
    
    # Load and clean data
    df_clean = load_and_clean_data()
    
    # Generate all visualizations
    q1_results = question_1_time_series_2011(df_clean)
    q2_results = question_2_top_countries(df_clean)
    q3_results = question_3_top_customers(df_clean)
    q4_results = question_4_demand_by_country(df_clean)
    
    # Export cleaned data
    export_cleaned_data(df_clean)
    
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE!")
    print("Generated visualizations:")
    print("- Q1_2011_Monthly_Revenue_Trend.png")
    print("- Q2_Top_10_Countries_Revenue_Quantity.png")
    print("- Q3_Top_10_Customers_Revenue.png")
    print("- Q4_Country_Demand_Analysis.png")
    print("\nCleaned data files:")
    print("- cleaned_retail_data.csv")
    print("- cleaned_retail_data_2011.csv")
    print("\nThese files can be imported into Tableau or Power BI for further analysis.")

if __name__ == "__main__":
    main()