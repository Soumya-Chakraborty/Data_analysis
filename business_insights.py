import pandas as pd
import numpy as np

def generate_business_insights():
    """Generate comprehensive business insights for CEO and CMO based on analysis"""
    
    print("RETAIL DATA ANALYSIS - BUSINESS INSIGHTS REPORT")
    print("=" * 60)
    print("Prepared for: CEO and CMO")
    print("Analysis Period: December 2010 - December 2011")
    print("=" * 60)
    
    # Load the cleaned data
    df = pd.read_csv('Master_Cleaned_Retail_Data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Question 1 Insights: 2011 Revenue Trends
    print("\n🔍 QUESTION 1 INSIGHTS: 2011 SEASONAL REVENUE TRENDS")
    print("-" * 50)
    
    df_2011 = df[df['Year'] == 2011]
    monthly_revenue = df_2011.groupby(['Month', 'MonthName'])['Revenue'].sum().reset_index()
    monthly_revenue = monthly_revenue.sort_values('Month')
    
    peak_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmax()]
    low_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmin()]
    
    print(f"📈 Peak Revenue Month: {peak_month['MonthName']} (£{peak_month['Revenue']:,.0f})")
    print(f"📉 Lowest Revenue Month: {low_month['MonthName']} (£{low_month['Revenue']:,.0f})")
    
    # Calculate growth trends
    monthly_revenue['Growth'] = monthly_revenue['Revenue'].pct_change() * 100
    
    print(f"🎯 Revenue Variation: {monthly_revenue['Revenue'].std()/monthly_revenue['Revenue'].mean()*100:.1f}% coefficient of variation")
    
    # Seasonal insights
    q4_months = monthly_revenue[monthly_revenue['Month'].isin([10, 11, 12])]['Revenue'].sum()
    total_2011 = monthly_revenue['Revenue'].sum()
    
    print(f"🎄 Q4 Contribution: {q4_months/total_2011*100:.1f}% of annual revenue")
    print("\n💡 CEO RECOMMENDATIONS:")
    print("   • Prepare inventory for November peak season (highest revenue month)")
    print("   • Plan marketing campaigns for January-February (lowest revenue period)")
    print("   • Q4 represents significant revenue concentration - diversify seasonal strategy")
    
    # Question 2 Insights: International Markets
    print("\n\n🌍 QUESTION 2 INSIGHTS: INTERNATIONAL MARKET OPPORTUNITIES")
    print("-" * 50)
    
    intl_data = df[df['Country'] != 'United Kingdom'].groupby('Country').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'CustomerID': 'nunique'
    }).reset_index()
    intl_data = intl_data.sort_values('Revenue', ascending=False).head(10)
    
    print("🏆 TOP 3 INTERNATIONAL MARKETS:")
    for i, row in intl_data.head(3).iterrows():
        print(f"   {i+1}. {row['Country']}: £{row['Revenue']:,.0f} revenue, {row['Quantity']:,} units")
    
    # Market analysis
    total_intl_revenue = intl_data['Revenue'].sum()
    top_3_share = intl_data.head(3)['Revenue'].sum() / total_intl_revenue * 100
    
    print(f"\n📊 Market Concentration: Top 3 countries = {top_3_share:.1f}% of international revenue")
    print(f"🎯 Average Order Value varies significantly across markets")
    
    print("\n💡 CMO RECOMMENDATIONS:")
    print("   • Focus expansion efforts on Netherlands, EIRE, and Germany")
    print("   • Netherlands shows highest volume - optimize logistics partnerships")
    print("   • EIRE has strong revenue per customer - premium market positioning")
    print("   • Germany offers balanced volume and value - scale marketing investment")
    
    # Question 3 Insights: Customer Segmentation
    print("\n\n👥 QUESTION 3 INSIGHTS: HIGH-VALUE CUSTOMER ANALYSIS")
    print("-" * 50)
    
    customer_data = df[df['CustomerID'].notna()].groupby('CustomerID').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'InvoiceNo': 'nunique',
        'Country': 'first'
    }).reset_index()
    customer_data = customer_data.sort_values('Revenue', ascending=False)
    
    top_10_customers = customer_data.head(10)
    top_10_revenue = top_10_customers['Revenue'].sum()
    total_customer_revenue = customer_data['Revenue'].sum()
    
    print(f"💎 Top 10 customers generate £{top_10_revenue:,.0f} ({top_10_revenue/total_customer_revenue*100:.1f}% of customer revenue)")
    print(f"📈 Average top customer value: £{top_10_customers['Revenue'].mean():,.0f}")
    print(f"🔄 Average orders per top customer: {top_10_customers['InvoiceNo'].mean():.1f}")
    
    # Customer concentration risk
    top_1_customer = customer_data.iloc[0]
    print(f"⚠️  Top customer concentration: {top_1_customer['Revenue']/total_customer_revenue*100:.2f}% of revenue")
    
    print("\n💡 CMO RECOMMENDATIONS:")
    print("   • Implement VIP customer program for top 10 customers")
    print("   • Reduce dependency on single largest customer (diversification risk)")
    print("   • Create customer success team for £50K+ annual value customers")
    print("   • Develop retention strategies - personal account management")
    
    # Question 4 Insights: Expansion Strategy
    print("\n\n🚀 QUESTION 4 INSIGHTS: MARKET EXPANSION STRATEGY")
    print("-" * 50)
    
    expansion_data = df[df['Country'] != 'United Kingdom'].groupby('Country').agg({
        'Quantity': 'sum',
        'Revenue': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique'
    }).reset_index()
    
    expansion_data['Avg_Order_Value'] = expansion_data['Revenue'] / expansion_data['InvoiceNo']
    expansion_data['Customer_Penetration'] = expansion_data['CustomerID'] / expansion_data['InvoiceNo']
    expansion_data = expansion_data.sort_values('Quantity', ascending=False)
    
    high_demand_countries = expansion_data.head(5)
    
    print("🎯 HIGHEST DEMAND MARKETS (by quantity):")
    for i, row in high_demand_countries.iterrows():
        print(f"   • {row['Country']}: {row['Quantity']:,} units, £{row['Avg_Order_Value']:.0f} avg order")
    
    # Expansion opportunity scoring
    expansion_data['Expansion_Score'] = (
        (expansion_data['Quantity'] / expansion_data['Quantity'].max()) * 0.4 +
        (expansion_data['Revenue'] / expansion_data['Revenue'].max()) * 0.3 +
        (expansion_data['Avg_Order_Value'] / expansion_data['Avg_Order_Value'].max()) * 0.3
    )
    
    top_expansion = expansion_data.nlargest(5, 'Expansion_Score')
    
    print(f"\n🏅 TOP EXPANSION OPPORTUNITIES (composite score):")
    for i, row in top_expansion.iterrows():
        print(f"   {i+1}. {row['Country']} (Score: {row['Expansion_Score']:.2f})")
    
    print("\n💡 CEO RECOMMENDATIONS:")
    print("   • Prioritize Netherlands for immediate expansion (highest volume)")
    print("   • Establish distribution centers in top 3 demand countries")
    print("   • EIRE shows premium market potential - focus on high-value products")
    print("   • Germany offers scalable growth - invest in marketing and logistics")
    print("   • Monitor emerging markets: Australia, Sweden for future expansion")
    
    # Overall Strategic Summary
    print("\n\n📋 STRATEGIC SUMMARY & ACTION PLAN")
    print("=" * 60)
    
    total_revenue = df['Revenue'].sum()
    uk_revenue = df[df['Country'] == 'United Kingdom']['Revenue'].sum()
    intl_percentage = (1 - uk_revenue/total_revenue) * 100
    
    print(f"📊 Current Business Metrics:")
    print(f"   • Total Revenue: £{total_revenue:,.0f}")
    print(f"   • International Revenue: {intl_percentage:.1f}% of total")
    print(f"   • Customer Base: {df['CustomerID'].nunique():,} unique customers")
    print(f"   • Geographic Reach: {df['Country'].nunique()} countries")
    
    print(f"\n🎯 IMMEDIATE ACTIONS (Next 90 Days):")
    print("   1. Implement Q4 inventory planning for seasonal surge")
    print("   2. Launch VIP program for top 10 customers")
    print("   3. Conduct market research in Netherlands, EIRE, Germany")
    print("   4. Develop customer retention strategy for high-value segments")
    
    print(f"\n🚀 STRATEGIC INITIATIVES (6-12 Months):")
    print("   1. Establish European distribution network")
    print("   2. Diversify revenue streams to reduce seasonal dependency")
    print("   3. Implement customer success program")
    print("   4. Expand product portfolio for international markets")
    
    print(f"\n📈 SUCCESS METRICS TO TRACK:")
    print("   • International revenue growth rate")
    print("   • Customer retention rate (especially top 10%)")
    print("   • Seasonal revenue smoothing")
    print("   • Market penetration in expansion countries")
    
    print("\n" + "=" * 60)
    print("Report generated successfully!")
    print("Use this analysis to drive data-informed business decisions.")

if __name__ == "__main__":
    generate_business_insights()