# Retail Data Visualization Guide
## Power BI & Tableau Implementation for CEO/CMO Analysis

### Overview
This guide provides step-by-step instructions for creating all four requested visualizations using the cleaned retail data. Each question addresses specific business needs from the CEO and CMO.

---

## Data Preparation Summary

**Files Available:**
- `Master_Cleaned_Retail_Data.csv` - Complete dataset with all derived fields
- `Q1_2011_Monthly_Data.csv` - Pre-aggregated monthly data for 2011
- `Q2_Countries_Revenue_Analysis.csv` - Country-level metrics (excluding UK)
- `Q3_Customer_Revenue_Analysis.csv` - Customer revenue rankings
- `Q4_Country_Demand_Analysis.csv` - Country demand analysis
- `Data_Dictionary.csv` - Field definitions and descriptions

**Data Quality Checks Applied:**
- ✅ Quantity >= 1 (removed 10,624 records)
- ✅ UnitPrice > £0 (removed 1,181 additional records)
- ✅ Revenue calculated as Quantity × UnitPrice

---

## Question 1: 2011 Monthly Revenue Trend Analysis

### Business Objective
CEO wants to view seasonal trends in 2011 revenue data for forecasting next year's performance.

### Power BI Implementation

**Step 1: Data Import**
1. Open Power BI Desktop
2. Get Data → Text/CSV → Select `Q1_2011_Monthly_Data.csv`
3. Verify data types:
   - Year: Whole Number
   - Month: Whole Number
   - MonthName: Text
   - Total_Revenue: Currency

**Step 2: Create Visualization**
1. Insert → Line Chart
2. Axis: Month (ensure sorted 1-12)
3. Values: Total_Revenue
4. Format:
   - Title: "2011 Monthly Revenue Trend - Seasonal Analysis"
   - Y-axis: Format as Currency (£)
   - Data labels: Show values
   - Line style: Increase thickness
   - Markers: Enable

**Step 3: Enhanced Features**
- Add trend line: Analytics → Trend line
- Add average line: Analytics → Average line
- Create month name labels: Use MonthName field for better readability

### Tableau Implementation

**Step 1: Data Connection**
1. Connect → Text File → Select `Q1_2011_Monthly_Data.csv`
2. Drag to data source area
3. Verify data types match Power BI specifications

**Step 2: Create Visualization**
1. Drag Month to Columns
2. Drag Total_Revenue to Rows
3. Change mark type to Line
4. Right-click Month → Sort → Ascending
5. Format:
   - Title: "2011 Monthly Revenue Trend - Seasonal Analysis"
   - Axis: Format Y-axis as Currency
   - Add reference lines for average and trend

**Step 3: Dashboard Enhancement**
- Add annotations for peak/low months
- Include sparklines for quick trend identification
- Add month-over-month growth calculations

---

## Question 2: Top 10 Countries Revenue & Quantity Analysis

### Business Objective
CMO wants to see top 10 revenue-generating countries (excluding UK) with quantity sold.

### Power BI Implementation

**Step 1: Data Import**
- Use `Q2_Countries_Revenue_Analysis.csv`
- Verify Total_Revenue: Currency, Total_Quantity: Whole Number

**Step 2: Create Dual-Axis Chart**
1. Insert → Combo Chart (Clustered Column and Line)
2. Shared Axis: Country
3. Column Values: Total_Revenue
4. Line Values: Total_Quantity
5. Filter: Revenue_Rank <= 10

**Step 3: Formatting**
- Title: "Top 10 Countries by Revenue and Quantity (Excluding UK)"
- Left Y-axis: Revenue (Currency format)
- Right Y-axis: Quantity
- Sort by Total_Revenue descending
- Color scheme: Blue for revenue bars, Orange for quantity line

### Tableau Implementation

**Step 1: Data Setup**
- Import `Q2_Countries_Revenue_Analysis.csv`
- Filter Revenue_Rank to Top 10

**Step 2: Dual-Axis Visualization**
1. Drag Country to Columns
2. Drag Total_Revenue to Rows
3. Drag Total_Quantity to Rows (creates dual axis)
4. Right-click second axis → Dual Axis
5. Right-click second axis → Synchronize Axis (uncheck)
6. Mark type: Bar for revenue, Line for quantity

**Step 3: Enhancement**
- Sort countries by revenue descending
- Format axes appropriately
- Add data labels for precise values
- Use different colors for clarity

---

## Question 3: Top 10 Customers Revenue Analysis

### Business Objective
CMO wants to identify highest revenue customers for targeted retention strategies.

### Power BI Implementation

**Step 1: Data Import**
- Use `Q3_Customer_Revenue_Analysis.csv`
- Filter Revenue_Rank <= 10

**Step 2: Create Horizontal Bar Chart**
1. Insert → Horizontal Bar Chart
2. Axis: CustomerID (format as "Customer XXXXX")
3. Values: Total_Revenue
4. Sort: Descending by Total_Revenue

**Step 3: Formatting**
- Title: "Top 10 Revenue Generating Customers"
- X-axis: Currency format
- Data labels: Show values
- Color gradient: Highest to lowest
- Add customer country information as tooltip

### Tableau Implementation

**Step 1: Data Preparation**
- Import customer data
- Create calculated field: "Customer " + STR([CustomerID])
- Filter to top 10 by revenue

**Step 2: Horizontal Bar Chart**
1. Drag calculated Customer field to Rows
2. Drag Total_Revenue to Columns
3. Sort by Total_Revenue descending
4. Format as horizontal bars

**Step 3: Additional Insights**
- Add Country as color
- Include Total_Quantity and Unique_Orders in tooltip
- Create customer value segmentation

---

## Question 4: Country Demand Analysis for Expansion

### Business Objective
CEO wants to identify countries with highest product demand for expansion planning.

### Power BI Implementation

**Step 1: Data Import**
- Use `Q4_Country_Demand_Analysis.csv`
- All countries except UK

**Step 2: Create Bubble Chart**
1. Insert → Scatter Chart
2. X-axis: Total_Revenue
3. Y-axis: Total_Quantity_Demanded
4. Size: Unique_Orders
5. Details: Country

**Step 3: Formatting**
- Title: "Country Demand Analysis - Expansion Opportunities"
- Format axes as Currency and Number
- Add country labels
- Use size legend for order volume
- Color by demand rank or region

### Tableau Implementation

**Step 1: Data Setup**
- Import Q4 dataset
- Exclude UK data

**Step 2: Bubble Chart Creation**
1. Drag Total_Revenue to Columns
2. Drag Total_Quantity_Demanded to Rows
3. Drag Country to Detail
4. Drag Unique_Orders to Size
5. Change mark type to Circle

**Step 3: Enhancement**
- Add country labels
- Format axes appropriately
- Use color to show additional dimension (e.g., Avg_Order_Value)
- Add reference lines for averages
- Create quadrant analysis (high/low revenue vs high/low demand)

---

## Advanced Analytics Recommendations

### Power BI DAX Measures
```dax
Revenue Growth = 
DIVIDE(
    [Current Month Revenue] - [Previous Month Revenue],
    [Previous Month Revenue]
)

Customer Lifetime Value = 
SUMX(
    VALUES(Customers[CustomerID]),
    [Total Revenue by Customer]
)
```

### Tableau Calculated Fields
```tableau
Revenue Growth Rate = 
(SUM([Revenue]) - LOOKUP(SUM([Revenue]), -1)) / LOOKUP(SUM([Revenue]), -1)

Seasonal Index = 
SUM([Revenue]) / WINDOW_AVG(SUM([Revenue]))
```

---

## Dashboard Design Best Practices

### Layout Recommendations
1. **Question 1**: Time series on top, with filters for year selection
2. **Question 2**: Side-by-side comparison with country selector
3. **Question 3**: Customer ranking with drill-down capabilities
4. **Question 4**: Geographic or bubble chart with expansion metrics

### Interactive Features
- Date range selectors
- Country/region filters
- Customer segment filters
- Export capabilities for executive reporting

### Performance Optimization
- Use aggregated datasets for better performance
- Implement incremental refresh for large datasets
- Optimize DAX/calculated fields
- Use appropriate visualization types for data size

---

## File Naming Convention for Submission

### Power BI Files
- Save as: `Retail_Analysis_Dashboard.pbix`
- Individual question files: `Q1_Revenue_Trend.pbix`, `Q2_Countries.pbix`, etc.

### Tableau Files
- Save as: `Retail_Analysis_Dashboard.twbx`
- Individual question files: `Q1_Revenue_Trend.twbx`, `Q2_Countries.twbx`, etc.

---

## Troubleshooting Common Issues

### Data Import Problems
- Ensure CSV files use UTF-8 encoding
- Check date formats are recognized correctly
- Verify numeric fields don't contain text

### Visualization Issues
- Sort axes appropriately for meaningful display
- Use appropriate scales for dual-axis charts
- Ensure filters are applied correctly

### Performance Issues
- Use data source filters instead of visualization filters when possible
- Aggregate data at appropriate levels
- Consider data modeling optimizations

---

This guide ensures consistent, professional visualizations that address each stakeholder's specific analytical needs while maintaining data integrity and visual clarity.