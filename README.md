# Mai Shan Yun Analytics Dashboard

A comprehensive business intelligence platform designed for Mai Shan Yun restaurant to optimize inventory management, forecast ingredient demand, and support data-driven business decisions.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Dashboard Pages](#dashboard-pages)
- [Datasets and Data Integration](#datasets-and-data-integration)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Example Insights and Use Cases](#example-insights-and-use-cases)
- [Future Enhancements](#future-enhancements)

## Overview

The Mai Shan Yun Analytics Dashboard transforms raw restaurant operational data into actionable business insights. Built with Streamlit and enhanced with Claude AI integration, this platform helps restaurant managers make informed decisions about inventory ordering, understand sales trends, and predict future ingredient needs with confidence.

### The Challenge

Managing restaurant inventory presents several critical challenges. Overstocking ties up capital and leads to waste from spoilage. Understocking creates stockouts that disappoint customers and result in lost revenue. Manual forecasting is time consuming and often inaccurate. Understanding seasonal demand patterns requires analyzing large amounts of historical data. These problems compound in busy restaurant environments where managers already juggle multiple operational responsibilities.

### Our Solution

This dashboard automates the entire inventory intelligence workflow. It continuously monitors ingredient levels against predicted usage rates, generates three month demand forecasts using statistical models, creates intelligent reorder alerts before stockouts occur, identifies seasonal trends to optimize purchasing, and provides AI powered recommendations in plain language that any manager can understand and act on immediately.

## Key Features

### Real Time Analytics

The system tracks key performance indicators including total orders, revenue, and growth rates in real time. Interactive visualizations make it easy to spot trends at a glance. Month over month comparisons help managers understand business trajectory and identify areas needing attention.

### Predictive Forecasting

Our forecasting engine generates three month demand predictions for all tracked ingredients. The system uses linear regression modeling with trend strength analysis to ensure reliability. Each forecast includes R squared confidence metrics so managers know which predictions to trust most. The platform automatically detects seasonal patterns including peak and low demand months.

### Intelligent Alert System

Automated reorder recommendations are generated based on forecasted usage rates rather than simple stock levels. The four tier alert system categorizes items as Critical (less than 3 days supply), Urgent (3 to 5 days), Reorder Soon (5 to 10 days), or Sufficient (more than 10 days). Days until depletion calculations enable proactive ordering before problems arise.

### AI Powered Insights

Integration with Claude AI provides natural language insights for any ingredient. The system generates personalized recommendations based on historical patterns, current inventory levels, and forecast data. Explanations are written for business users without technical backgrounds. Complete insight reports can be downloaded for record keeping or sharing with suppliers.

### Comprehensive Analysis

The platform analyzes sales trends by category and time period to inform menu decisions. Inventory status monitoring includes detailed usage patterns for all ingredients. Shipment optimization recommendations help reduce delivery costs. Cost driver analysis supports budgeting and financial planning.

## Dashboard Pages

### Overview

The overview page provides a high level snapshot of restaurant performance. Key metrics include total orders with month over month growth percentages, revenue trends and growth rates, the count of ingredients currently being tracked (14 core items), and the number of items requiring immediate reorder attention.

Visualizations on this page include a monthly orders trend line showing business volume over time, a revenue trend chart with area fill for visual impact, a bar chart of top selling categories, and an inventory alerts table showing which items need attention with their specific reorder timelines.

This page serves as the daily morning review dashboard. Managers can quickly understand overall business health and identify immediate action items requiring attention before the day begins.

### Sales Analysis

The sales analysis page offers a deep dive into performance by menu category. It displays trends for the top 10 categories over time and highlights top performers. Current data shows Ramen at 31.4% of sales, Fried Chicken at 26.1%, and Lunch Special at 19.9%. Category comparison charts help managers understand the sales mix.

Visualizations include a multi line chart showing category sales over time, pie charts displaying the distribution of top and bottom performing categories, and clean professional presentations with automatic filtering of placeholder categories.

This analysis supports menu optimization decisions, promotional planning, and helps managers understand customer preferences and spending patterns.

### Inventory Management

The inventory management page monitors ingredient levels and usage patterns comprehensively. Key metrics displayed include total ingredients tracked (14 core items), total historical usage (588,308 grams), average weekly usage based on forecasts (10,024 grams), and the count of items currently needing reorder (typically 8 critical items).

The page features an alert status distribution pie chart, a histogram showing days until depletion across all ingredients, a complete ingredient status report with units clearly displayed, and a horizontal bar chart of the top 10 ingredients by historical usage volume.

Alert categories are color coded for quick scanning. Red indicates critical items requiring urgent reorder (less than 3 days supply). Yellow marks items to reorder soon (3 to 10 days supply). Green shows sufficient stock (more than 10 days supply). Blue indicates unknown status when shipment data is unavailable.

Managers use this page for weekly inventory reviews, preparing supplier orders, and identifying opportunities to reduce waste through better ordering patterns.

### Shipment Management

The shipment management page helps optimize delivery schedules and order quantities. Current metrics show 61 total monthly deliveries, an average quantity per shipment of 5,519.9 grams, and 11.8 deliveries per week across all suppliers.

The page displays monthly shipment frequency by ingredient in an interactive bar chart, average shipment quantity analysis to identify ordering patterns, a reorder recommendations table based on forecast data, and supplier coordination insights.

This analysis helps managers negotiate better delivery schedules, consolidate orders to reduce costs, and ensure optimal order quantities that balance holding costs against delivery fees.

### Demand Forecasting and AI Insights

The forecasting page predicts future demand and provides AI powered recommendations. Top level metrics show 14 ingredients forecasted, the forecast period of November 2025 through January 2026, 4 ingredients with strong reliable trends, and 6 items requiring critical reorders based on predictions.

For each ingredient selected, the system displays historical average usage, forecasted average for the next three months, peak usage recorded, and volatility measured as standard deviation.

Visualizations include a time series chart overlaying historical data with three month forecasts, trend lines showing visual regression analysis, seasonal pattern summaries with peak and low months plus variation percentages, and a heatmap comparing usage across all ingredients.

The AI insights generator works simply. Select any ingredient from the dropdown menu, click the generate insights button, and receive a comprehensive analysis within seconds. The AI provides key findings based on data patterns, explains business implications in plain language, recommends specific actions to take, and alerts managers to potential risks worth monitoring.

This page supports monthly planning sessions, budget forecasting, seasonal menu adjustments, and supplier negotiations. The AI insights help even non technical managers understand complex data patterns and make confident decisions.

## Datasets and Data Integration

### Core Data Files

The system integrates 13 distinct data files covering different aspects of restaurant operations.

The analytics KPI summary file contains 6 rows of monthly performance data including order counts, revenue amounts, and growth percentages for each metric. This provides the foundation for trend analysis.

The historical demand file holds 168 rows tracking past ingredient usage with columns for ingredient name, time period, quantity value, unit of measurement, and data type classification. This historical record enables accurate forecasting.

The demand forecast file contains 42 rows of AI generated predictions including ingredient name, future time periods, forecasted usage amounts, trend strength classifications, and R squared reliability scores.

The reorder alerts file tracks 14 ingredients with current status including total usage, forecasted days until depletion, and color coded alert levels. This drives the proactive reordering system.

Sales category monthly data spans 264 rows showing category performance over time with order counts by menu category and time period. This supports menu optimization decisions.

Additional files track top and bottom performing categories (30 rows each), shipment patterns for all ingredients (14 rows), seasonal trends with peak and low months (14 rows), forecast metadata (14 rows), cost drivers (14 rows), recipe compositions (170+ rows), and raw shipment records (14 rows).

### Data Integration Flow

The data pipeline starts with raw sales data from the POS system. This feeds into a data processing layer built with Python and Pandas that performs aggregation, normalization, and time series preparation.

Processed data flows to the forecasting engine which applies linear regression, conducts seasonal analysis, and detects trend patterns. The forecasting output feeds the alert generation system that calculates days until depletion, applies reorder thresholds, and classifies status levels.

Finally, all processed data and insights display in the Streamlit dashboard with real time updates, interactive filtering capabilities, and on demand AI insight generation.

### Units of Measurement

The dashboard intelligently handles multiple unit types. Most ingredients measure in grams including rice, vegetables, and proteins. Countable items like eggs and ramen packages use count units. Generic items use the units designation. Individual portions measure in pieces. All visualizations and tables display units inline with values to prevent confusion.

## Technologies Used

### Core Framework

The application runs on Streamlit version 1.28 or higher, a modern web framework perfect for data applications. Python 3.9 or higher provides the foundational programming environment.

### Data Analysis and Visualization

Pandas handles all data manipulation and analysis operations. NumPy performs numerical computations efficiently. Plotly creates interactive charts and graphs through both its express module for high level plotting and graph objects module for custom visualizations.

### AI Integration

The system connects to Anthropic Claude API through OpenRouter to generate insights. We use the Claude 3.7 Sonnet model which excels at natural language understanding and business recommendation generation.

### Additional Libraries

The requests library manages API calls to Claude. Standard datetime functions handle time based operations. OS utilities manage environment variables securely.

## Setup Instructions

### Prerequisites

You need Python version 3.9 or higher installed on your system. The pip package manager should be available. If you want to use AI insights, obtain an OpenRouter API key.

### Step 1: Organize Project Files

Create a project directory and download all required files into it. Your folder structure should contain the main dashboard Python file, all 13 CSV data files, and this README file. Keeping everything in one directory simplifies the setup process.

### Step 2: Install Dependencies

We recommend creating a virtual environment to avoid conflicts with other Python projects. On Windows, run python -m venv venv then activate it with venv\Scripts\activate. On macOS or Linux, use source venv/bin/activate after creating the environment.

Install required packages with pip install streamlit pandas plotly numpy requests. Alternatively, create a requirements.txt file with the package specifications and run pip install -r requirements.txt.

The requirements file should specify streamlit version 1.28.0 or higher, pandas version 2.0.0 or higher, plotly version 5.17.0 or higher, numpy version 1.24.0 or higher, and requests version 2.31.0 or higher.

### Step 3: Configure API Key (Optional)

The AI insights feature requires an OpenRouter API key but the dashboard works without it. To enable insights, set an environment variable named OPENROUTER_API_KEY.

On Windows Command Prompt, use set OPENROUTER_API_KEY=your_api_key_here. On Windows PowerShell, use $env:OPENROUTER_API_KEY="your_api_key_here". On macOS or Linux, use export OPENROUTER_API_KEY=your_api_key_here.

Alternatively, create a .env file in your project directory containing OPENROUTER_API_KEY=your_api_key_here.

To obtain an API key, visit OpenRouter.ai and sign up for an account. Generate an API key through their dashboard and add credits to your account. Five dollars is recommended for initial testing.

Without an API key configured, all dashboard features work normally except the AI insights generation button will display an error message.

### Step 4: Run the Dashboard

Start the application by running streamlit run dashboard_corrected.py from your project directory. The dashboard opens automatically in your default web browser at localhost port 8501.

### Troubleshooting Common Issues

If you see errors about missing CSV files, verify that all data files are in the same directory as the dashboard Python file. The application expects to find them in the current working directory.

Module not found errors indicate a missing package. Install it with pip install followed by the package name shown in the error message.

If port 8501 is already in use by another application, specify a different port with streamlit run dashboard_corrected.py --server.port 8502.

## Usage Guide

### Navigation

The sidebar on the left provides navigation between five main pages: Overview for daily snapshots, Sales Analysis for category performance, Inventory for stock monitoring, Shipments for delivery optimization, and Forecasting for predictions and AI insights.

### Interactive Features

Charts respond to mouse hovers displaying exact values. Trend lines show data for each time period. Bar charts reveal precise counts or quantities. Pie charts display percentages and category names.

The forecasting page includes an ingredient selection dropdown. Choose any of the 14 tracked ingredients to view historical patterns and future predictions. Compare metrics across different ingredients by switching selections.

AI insights generation works through a simple three step process. Navigate to the Forecasting page, select an ingredient from the dropdown, and click the generate insights button. Wait 5 to 10 seconds while Claude analyzes the data. Review the comprehensive recommendations provided. Download insights as a text file for future reference or sharing with team members.

Tables throughout the dashboard automatically sort by priority metrics such as days until depletion. Alert status appears in color coded format for quick scanning. Pie charts automatically filter out zero value placeholder categories to present clean meaningful visualizations.

### Best Practices

Daily routines should include checking the Overview page for critical alerts, reviewing items with less than 3 days supply remaining, and placing urgent orders identified by the system.

Weekly routines benefit from a complete Inventory page review. Check items with 3 to 10 days supply and plan supplier orders for the coming week. Review shipment patterns to identify optimization opportunities.

Monthly routines should analyze Sales Analysis trends comprehensively. Generate AI insights for your top 3 ingredients by volume. Review the Forecasting page for all items to understand upcoming needs. Adjust menu offerings based on identified seasonal patterns. Update supplier agreements based on volume projections and cost driver analysis.

## Example Insights and Use Cases

### Preventing Stockouts

Consider a scenario where the restaurant runs out of cilantro during the dinner rush. This creates disappointed customers and forces menu modifications that reduce revenue.

The dashboard provides multiple warnings before this happens. The Inventory page shows cilantro with a critical red alert indicating only 1.2 days of supply remain. The Forecasting page predicts weekly usage of 6,717 grams based on historical patterns. The AI generates a specific insight: "Order 14,000 grams immediately to cover the next two weeks. Increase your standard order quantity to 20,000 grams to provide a safety buffer. Consider switching to twice weekly deliveries during peak season."

Following these recommendations prevents the stockout entirely, maintains full menu availability, and improves customer satisfaction.

### Optimizing Menu Mix

Imagine the restaurant is considering whether to expand fried chicken offerings with new premium options. This represents a significant investment in recipe development and marketing.

The Sales Analysis page shows fried chicken currently represents 26.1% of total sales, making it the second highest category. The Overview page reveals 15% growth month over month, indicating increasing popularity. The Forecasting page predicts sustained high demand through the next quarter with a strong trend classification.

The AI insight provides strategic guidance: "Fried chicken shows strong upward trend with high customer preference scores. Your data supports expansion in this category. Consider adding a premium fried chicken option at a higher price point. Bundle offerings with appetizers to increase average ticket size. Plan a promotional campaign for Q1 when historical data shows peak demand. Estimated revenue increase of 12% if executed well."

This data driven recommendation gives management confidence to invest in menu expansion with clear projections of expected returns.

### Seasonal Planning

A restaurant planning winter menu changes needs to understand how demand patterns shift with the seasons.

The Seasonal Trends analysis reveals rice usage peaks in December with a 45% increase versus summer months. The Forecasting page predicts average monthly usage of 119,023 grams during winter. Historical data confirms this pattern has repeated consistently over multiple years.

The AI generates a comprehensive seasonal plan: "Winter months consistently show 45% increase in rice based dishes, likely due to customer preference for hot comfort foods. Recommendations for upcoming season: Increase December rice order to 150,000 grams to ensure adequate supply. Negotiate volume discount with your supplier based on predictable high volume period. Stock up in November to avoid rush pricing and potential supply constraints. Promote hot soup specials which drive rice sales. Consider temporary winter menu additions featuring rice to capitalize on natural demand increase."

Following this plan ensures the restaurant is prepared for the seasonal spike, secures better pricing through early negotiation, and maximizes revenue through targeted promotions.

### Reducing Costs

The restaurant wants to reduce operational costs without compromising service quality. Delivery fees represent a significant expense.

The Shipments page reveals 61 monthly deliveries averaging 11.8 per week. The Cost Drivers analysis suggests current delivery frequency exceeds operational needs. The Forecast data confirms safety stock can be maintained with fewer deliveries if order quantities increase appropriately.

The AI provides specific optimization recommendations: "Current delivery frequency is higher than operationally necessary based on usage rates and storage capacity. Consolidate carrot and peas shipments since they come from the same supplier. Increase individual order sizes by 40% while reducing delivery frequency by 50%. This maintains identical safety stock levels while cutting delivery trips in half. Projected savings of $800 per month in delivery fees. Additional benefit of reduced receiving labor costs. Recommend renegotiating supplier agreement to formalize new delivery schedule."

Implementation of these changes reduces costs by 30% while maintaining or improving inventory levels through larger safety buffers.

### Reducing Waste

High food waste from over ordering is both environmentally problematic and financially costly.

The Inventory analysis shows white onion with a green sufficient status indicating 13.4 days of supply available. The Forecasting page reveals a decreasing trend with current usage running 12% below historical averages. The AI detects an over ordering pattern that has developed.

The AI generates waste reduction recommendations: "White onion usage is declining but order quantities have not adjusted accordingly. Current order size exceeds actual needs based on recent demand patterns. Reduce order quantity from 12 kilograms to 8 kilograms, a 33% reduction. Extend reorder interval from 7 days to 10 days based on new usage rate. Continue monitoring for trend reversal that might indicate temporary rather than permanent decline. Projected waste reduction of 15% per month. Additional benefit of fresher ingredients since stock turns over faster. Consider customer feedback to determine if menu changes are driving the decline."

Following these recommendations reduces waste, frees up capital for other uses, and actually improves ingredient freshness through faster turnover.

## Future Enhancements

### Near Term Improvements

The next phase will add support for multiple restaurant locations managed from a single dashboard. Mobile applications for iOS and Android will enable on the go monitoring. Automated email alerts will notify managers of critical reorders without requiring dashboard login. Direct API integration with suppliers will enable automatic reorder placement. A recipe cost calculator will provide real time dish profitability analysis.

### Medium Term Additions

Advanced machine learning models including ARIMA and Facebook Prophet will improve forecast accuracy. Weather data integration will adjust predictions based on forecast conditions. Customer preference learning algorithms will optimize menu offerings automatically. Detailed waste tracking will identify specific spoilage patterns. Staff scheduling recommendations will align labor costs with predicted demand.

### Long Term Vision

Voice command integration will enable queries like asking Alexa what needs reordering. Predictive equipment maintenance will track lifecycle patterns for kitchen equipment. Market price intelligence will dynamically compare supplier offerings. Automated menu engineering will continuously analyze profitability by dish. Customer sentiment analysis through social media integration will connect online feedback to operational decisions.

## Contributing

This dashboard was custom built for Mai Shan Yun restaurant operations. For feature requests or bug reports, document the issue with screenshots if possible, provide example data demonstrating the problem, suggest potential solutions if you have ideas, and submit through email or your preferred project management tool.

## Credits

This platform was developed specifically for Mai Shan Yun restaurant operations. The AI capabilities are powered by Anthropic Claude 3.7 Sonnet accessed through the OpenRouter API. The web framework is built on Streamlit. Data analysis leverages Pandas, NumPy, and Plotly libraries.

## Quick Start Checklist

Before using the dashboard, verify you have Python 3.9 or higher installed. Confirm all CSV files are present in your project directory. Install dependencies using the requirements file. Configure your OpenRouter API key if you want AI insights enabled. Start the dashboard with the streamlit run command. Navigate through all five pages to familiarize yourself with the layout. Generate an AI insight for one ingredient to test the functionality. Review any critical reorder alerts requiring immediate attention. Bookmark the dashboard URL for quick daily access.

The system is designed to run continuously during business hours. Many managers keep it open on a dedicated monitor in the office for constant visibility into operations.

Last Updated: November 2025
