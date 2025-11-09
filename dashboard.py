import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
import requests

# Page configuration
st.set_page_config(
    page_title="Mai Shan Yun Analytics Dashboard",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 2px solid #1f77b4;
        font-size: 2.5rem !important;
        white-space: nowrap;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: normal;
        color: #000;
    }
    .metric-label {
        font-size: 0.875rem;
        font-weight: bold;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .metric-unit {
        font-size: 1rem;
        color: #666;
        margin-left: 4px;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to get unit for ingredient
def get_unit_for_ingredient(ingredient, data):
    """Get the unit of measurement for an ingredient"""
    if 'historical_demand' in data:
        matching = data['historical_demand'][data['historical_demand']['ingredient'] == ingredient]
        if not matching.empty:
            unit = matching.iloc[0]['unit']
            return unit if pd.notna(unit) else 'units'
    
    if 'demand_forecast' in data:
        matching = data['demand_forecast'][data['demand_forecast']['ingredient'] == ingredient]
        if not matching.empty:
            unit = matching.iloc[0]['unit']
            return unit if pd.notna(unit) else 'units'
    
    return 'units'

# Load data with caching
@st.cache_data
def load_data():
    """Load all CSV files from current directory"""
    try:
        kpi_summary = pd.read_csv('analytics_kpi_summary.csv')
        top5_categories = pd.read_csv('analytics_top5_categories.csv')
        bottom5_categories = pd.read_csv('analytics_bottom5_categories.csv')
        historical_demand = pd.read_csv('historical_demand.csv')
        shipment_summary = pd.read_csv('analytics_shipment_summary.csv')
        reorder_alerts = pd.read_csv('reorder_alerts.csv')
        ingredient_bom = pd.read_csv('ingredient_bom_long.csv')
        sales_category = pd.read_csv('sales_category_monthly.csv')
        shipments_clean = pd.read_csv('shipments_clean.csv')
        demand_forecast = pd.read_csv('demand_forecast_3months.csv')
        forecast_summary = pd.read_csv('forecast_summary.csv')
        seasonal_trends = pd.read_csv('seasonal_trends.csv')
        cost_drivers = pd.read_csv('cost_drivers.csv')
        
        # Parse dates
        kpi_summary['period'] = pd.to_datetime(kpi_summary['period'])
        top5_categories['period'] = pd.to_datetime(top5_categories['period'])
        bottom5_categories['period'] = pd.to_datetime(bottom5_categories['period'])
        historical_demand['period'] = pd.to_datetime(historical_demand['period'])
        sales_category['period'] = pd.to_datetime(sales_category['period'])
        demand_forecast['period'] = pd.to_datetime(demand_forecast['period'])
        
        return {
            'kpi_summary': kpi_summary,
            'top5_categories': top5_categories,
            'bottom5_categories': bottom5_categories,
            'historical_demand': historical_demand,
            'shipment_summary': shipment_summary,
            'reorder_alerts': reorder_alerts,
            'ingredient_bom': ingredient_bom,
            'sales_category': sales_category,
            'shipments_clean': shipments_clean,
            'demand_forecast': demand_forecast,
            'forecast_summary': forecast_summary,
            'seasonal_trends': seasonal_trends,
            'cost_drivers': cost_drivers
        }
    except FileNotFoundError as e:
        st.error(f"❌ Missing file: {e.filename}")
        st.info("Make sure all CSV files are in the same directory as the dashboard")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Claude AI Agent Function
def call_claude_agent(prompt, context_data):
    """Call Claude AI via OpenRouter API to generate insights"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        return "⚠️ Error: OPENROUTER_API_KEY environment variable not set. Please set it to use the AI agent."
    
    try:
        full_prompt = f"""You are a restaurant analytics expert helping Mai Shan Yun restaurant understand their ingredient usage and forecasts.

**Context Data:**
{context_data}

**User Request:**
{prompt}

Please provide clear, actionable insights that anyone can understand, even without technical knowledge. Use simple language and explain any technical terms. Structure your response with:
1. Key Findings (bullet points)
2. What This Means For The Restaurant
3. Recommended Actions
4. Potential Risks to Watch Out For

Keep it concise and practical."""

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3.7-sonnet",
                "messages": [{"role": "user", "content": full_prompt}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Error calling AI: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Initialize data
data = load_data()

if data is None:
    st.stop()

# Sidebar
st.sidebar.title("🍜 Mai Shan Yun")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Overview", "📈 Sales Analysis", "🥗 Inventory", "📦 Shipments", "🔮 Forecasting"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Dashboard Features:**
- Real-time KPIs
- Sales trends analysis
- Inventory monitoring
- Reorder recommendations
- 3-month demand forecasting
- AI-powered insights
""")

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "📊 Overview":
    st.title("📊 Restaurant Analytics Overview")
    
    kpi_df = data['kpi_summary']
    latest_period = kpi_df['period'].max()
    latest_data = kpi_df[kpi_df['period'] == latest_period].iloc[0]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        count_change = latest_data.get('count_mom_growth_%', 0)
        st.metric(
            "Total Orders",
            f"{int(latest_data['count']):,}",
            f"{count_change:.1f}%" if pd.notna(count_change) else None
        )
    
    with col2:
        amount = latest_data.get('amount', 0)
        amount_change = latest_data.get('amount_mom_growth_%', 0)
        st.metric(
            "Revenue",
            f"${amount:,.0f}",
            f"{amount_change:.1f}%" if pd.notna(amount_change) else None
        )
    
    with col3:
        total_ingredients = len(data['reorder_alerts'])
        st.metric("Ingredients Tracked", total_ingredients)
    
    with col4:
        alerts = data['reorder_alerts'][
            data['reorder_alerts']['forecasted_alert'].str.contains('Critical|Urgent|Soon', na=False)
        ].shape[0]
        st.metric("Reorder Alerts", alerts, delta_color="inverse")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Monthly Orders Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=kpi_df['period'],
            y=kpi_df['count'],
            mode='lines+markers',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8),
            name='Orders'
        ))
        fig.update_layout(height=350, showlegend=False, yaxis_title="Number of Orders", xaxis_title="Month")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Monthly Revenue Trend")
        if 'amount' in kpi_df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=kpi_df['period'],
                y=kpi_df['amount'],
                mode='lines+markers',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                name='Revenue'
            ))
            fig.update_layout(height=350, showlegend=False, yaxis_title="Revenue ($)", xaxis_title="Month")
            st.plotly_chart(fig, use_container_width=True)
    
    # Top categories
    st.markdown("### 🏆 Top Categories by Order Volume")
    top5_df = data['top5_categories']
    top5_latest = top5_df[top5_df['period'] == latest_period].sort_values('count', ascending=False)
    
    if not top5_latest.empty:
        fig = px.bar(
            top5_latest,
            x='group',
            y='count',
            color='count',
            color_continuous_scale='Blues',
            labels={'count': 'Number of Orders', 'group': 'Category'}
        )
        fig.update_layout(height=400, showlegend=False, xaxis_title="Category", yaxis_title="Number of Orders")
        st.plotly_chart(fig, use_container_width=True)
    
    # Alerts with UNITS
    st.markdown("### ⚠️ Inventory Reorder Alerts")
    reorder_df = data['reorder_alerts']
    alert_df = reorder_df[reorder_df['forecasted_alert'].str.contains('Critical|Urgent|Soon', na=False)].copy()
    
    if not alert_df.empty:
        display_df = alert_df[['ingredient', 'forecasted_weekly_usage', 'forecasted_days_until_depletion', 'forecasted_alert']].copy()
        display_df = display_df.sort_values('forecasted_days_until_depletion')
        
        # Add units inline with values
        display_df['unit'] = display_df['ingredient'].apply(lambda x: get_unit_for_ingredient(x, data))
        display_df['Weekly Usage (Forecasted)'] = display_df.apply(
            lambda row: f"{row['forecasted_weekly_usage']:,.1f} {row['unit']}", axis=1
        )
        display_df['Days Until Empty'] = display_df['forecasted_days_until_depletion'].round(1)
        
        display_df = display_df[['ingredient', 'Weekly Usage (Forecasted)', 'Days Until Empty', 'forecasted_alert']]
        display_df.columns = ['Ingredient', 'Weekly Usage (Forecasted)', 'Days Until Empty', 'Alert Status']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ All inventory levels are currently sufficient!")

# ============================================================================
# PAGE 2: SALES ANALYSIS
# ============================================================================
elif page == "📈 Sales Analysis":
    st.title("📈 Sales Performance Analysis")
    
    sales_df = data['sales_category']
    
    # Sales trend
    st.markdown("### 📊 Sales Trend by Category (Top 10)")
    category_sales = sales_df[sales_df['group'].notna()].copy()
    top_categories = category_sales.groupby('group')['count'].sum().nlargest(10).index
    category_sales_filtered = category_sales[category_sales['group'].isin(top_categories)]
    
    fig = px.line(
        category_sales_filtered,
        x='period',
        y='count',
        color='group',
        labels={'count': 'Number of Orders', 'period': 'Month', 'group': 'Category'}
    )
    fig.update_layout(height=450, legend_title_text='Category')
    st.plotly_chart(fig, use_container_width=True)
    
    # Category comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top Performing Categories")
        top5_df = data['top5_categories']
        top5_agg = top5_df.groupby('group')['count'].sum().sort_values(ascending=False).head(5)
        
        # Filter out zero values
        top5_agg_nonzero = top5_agg[top5_agg > 0]
        
        if len(top5_agg_nonzero) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=top5_agg_nonzero.index,
                values=top5_agg_nonzero.values,
                hole=0.3,
                textinfo='label+percent',
                textposition='auto',
                textfont=dict(size=12),
                marker=dict(line=dict(color='#000000', width=1))
            )])
            fig.update_layout(
                height=400,
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Lower Volume Categories")
        bottom5_df = data['bottom5_categories']
        bottom5_agg = bottom5_df.groupby('group')['count'].sum().sort_values(ascending=True).head(5)
        
        # Filter out zero values
        bottom5_agg_nonzero = bottom5_agg[bottom5_agg > 0]
        
        if len(bottom5_agg_nonzero) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=bottom5_agg_nonzero.index,
                values=bottom5_agg_nonzero.values,
                hole=0.3,
                textinfo='label+percent',
                textposition='auto',
                textfont=dict(size=12),
                marker=dict(line=dict(color='#000000', width=1))
            )])
            fig.update_layout(
                height=400,
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 3: INVENTORY
# ============================================================================
elif page == "🥗 Inventory":
    st.title("🥗 Inventory Management")
    
    reorder_df = data['reorder_alerts']
    
    # Summary metrics - WITH UNITS INLINE - CORRECTED
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Total Ingredients</div><div class="metric-value">{len(reorder_df)}</div></div>', unsafe_allow_html=True)
    
    with col2:
        total_usage_g = reorder_df['total_usage'].sum()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Total Usage (Historical)</div><div class="metric-value">{total_usage_g:,.0f} g</div></div>', unsafe_allow_html=True)
    
    with col3:
        avg_weekly_g = reorder_df['forecasted_weekly_usage'].mean()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Avg Weekly Usage (Forecast)</div><div class="metric-value">{avg_weekly_g:,.0f} g</div></div>', unsafe_allow_html=True)
    
    with col4:
        alerts = reorder_df[reorder_df['forecasted_alert'].str.contains('Critical|Urgent|Soon', na=False)].shape[0]
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Items Need Reorder</div><div class="metric-value">{alerts}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Status distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Alert Status Distribution (Forecasted)")
        alert_counts = reorder_df['forecasted_alert'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=alert_counts.index,
            values=alert_counts.values,
            hole=0.3,
            textinfo='label+percent',
            textposition='auto',
            textfont=dict(size=11),
            marker=dict(line=dict(color='#000000', width=1))
        )])
        fig.update_layout(
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Days Until Depletion Distribution")
        valid_days = reorder_df[reorder_df['forecasted_days_until_depletion'].notna()]['forecasted_days_until_depletion']
        if len(valid_days) > 0:
            fig = go.Figure(data=[go.Histogram(
                x=valid_days,
                nbinsx=20,
                marker=dict(color='#1f77b4', line=dict(color='#000000', width=1))
            )])
            fig.update_layout(
                height=350,
                xaxis_title="Days Until Empty",
                yaxis_title="Number of Ingredients",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Inventory table - WITH UNITS INLINE
    st.markdown("### 📋 Complete Ingredient Status Report")
    display_df = reorder_df[['ingredient', 'total_usage', 'forecasted_weekly_usage', 'forecasted_days_until_depletion', 'forecasted_alert']].copy()
    display_df = display_df.sort_values('forecasted_days_until_depletion')
    
    # Add units inline
    display_df['unit'] = display_df['ingredient'].apply(lambda x: get_unit_for_ingredient(x, data))
    display_df['Total Usage (Historical)'] = display_df.apply(
        lambda row: f"{row['total_usage']:,.1f} {row['unit']}", axis=1
    )
    display_df['Weekly Usage (Forecast)'] = display_df.apply(
        lambda row: f"{row['forecasted_weekly_usage']:,.1f} {row['unit']}", axis=1
    )
    display_df['Days Until Empty'] = display_df['forecasted_days_until_depletion'].round(1)
    
    display_df = display_df[['ingredient', 'Total Usage (Historical)', 'Weekly Usage (Forecast)', 'Days Until Empty', 'forecasted_alert']]
    display_df.columns = ['Ingredient', 'Total Usage (Historical)', 'Weekly Usage (Forecast)', 'Days Until Empty', 'Alert Status']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Top usage - WITH UNITS
    st.markdown("### 🔝 Top 10 Ingredients by Total Historical Usage")
    top_ingredients = reorder_df.nlargest(10, 'total_usage').copy()
    top_ingredients['unit'] = top_ingredients['ingredient'].apply(lambda x: get_unit_for_ingredient(x, data))
    top_ingredients['label'] = top_ingredients['ingredient'] + ' (' + top_ingredients['unit'] + ')'
    
    fig = px.bar(
        top_ingredients,
        x='total_usage',
        y='label',
        orientation='h',
        color='total_usage',
        color_continuous_scale='Viridis',
        labels={'label': 'Ingredient', 'total_usage': 'Total Usage'}
    )
    fig.update_layout(height=500, showlegend=False, yaxis_title="", xaxis_title="Total Historical Usage")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 4: SHIPMENTS
# ============================================================================
elif page == "📦 Shipments":
    st.title("📦 Shipment Management")
    
    shipment_df = data['shipment_summary']
    reorder_df = data['reorder_alerts']
    
    # Metrics - WITH UNITS INLINE
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_shipments = shipment_df['number_of_shipments'].sum()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Total Monthly Shipments</div><div class="metric-value">{int(total_shipments)}</div></div>', unsafe_allow_html=True)
    
    with col2:
        avg_qty_g = shipment_df['avg_quantity_per_shipment_grams'].mean()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Avg Quantity per Shipment</div><div class="metric-value">{avg_qty_g:,.1f} g</div></div>', unsafe_allow_html=True)
    
    with col3:
        weekly = (1 / shipment_df['weeks_between_shipments']).sum()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Total Weekly Shipments</div><div class="metric-value">{weekly:.1f}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Monthly Shipment Frequency by Ingredient")
        fig = px.bar(
            shipment_df.sort_values('number_of_shipments', ascending=False),
            x='ingredient',
            y='number_of_shipments',
            color='number_of_shipments',
            color_continuous_scale='Blues',
            labels={'number_of_shipments': 'Shipments per Month', 'ingredient': 'Ingredient'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False, yaxis_title="Shipments per Month")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📦 Average Shipment Quantity by Ingredient")
        fig = px.bar(
            shipment_df.sort_values('avg_quantity_per_shipment_grams', ascending=False),
            x='ingredient',
            y='avg_quantity_per_shipment_grams',
            color='avg_quantity_per_shipment_grams',
            color_continuous_scale='Greens',
            labels={'avg_quantity_per_shipment_grams': 'Quantity (grams)', 'ingredient': 'Ingredient'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False, yaxis_title="Average Quantity (g)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Reorder recommendations - WITH UNITS INLINE
    st.markdown("### ⚠️ Reorder Recommendations Based on Forecast")
    needs_reorder = reorder_df[reorder_df['forecasted_alert'].str.contains('Critical|Urgent|Soon', na=False)].copy()
    
    if not needs_reorder.empty:
        needs_reorder['unit'] = needs_reorder['ingredient'].apply(lambda x: get_unit_for_ingredient(x, data))
        needs_reorder['Weekly Usage (Forecasted)'] = needs_reorder.apply(
            lambda row: f"{row['forecasted_weekly_usage']:,.1f} {row['unit']}", axis=1
        )
        needs_reorder['Days Until Empty'] = needs_reorder['forecasted_days_until_depletion'].round(1)
        
        display_df = needs_reorder[['ingredient', 'Weekly Usage (Forecasted)', 'Days Until Empty', 'forecasted_alert']].copy()
        display_df = display_df.sort_values('Days Until Empty')
        display_df.columns = ['Ingredient', 'Weekly Usage (Forecasted)', 'Days Until Empty', 'Alert Status']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ All ingredient levels are currently sufficient!")

# ============================================================================
# PAGE 5: FORECASTING (ENHANCED)
# ============================================================================
elif page == "🔮 Forecasting":
    st.title("🔮 Demand Forecasting & AI Insights")
    
    historical_df = data['historical_demand']
    forecast_df = data['demand_forecast']
    forecast_summary_df = data['forecast_summary']
    seasonal_df = data['seasonal_trends']
    cost_df = data['cost_drivers']
    
    # Forecast period
    forecast_period_start = forecast_df['period'].min()
    forecast_period_end = forecast_df['period'].max()
    
    # Top metrics - CORRECTED: uniform heading style and single line forecast period
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ingredients = forecast_df['ingredient'].nunique()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Ingredients Forecasted</div><div class="metric-value">{total_ingredients}</div></div>', unsafe_allow_html=True)
    
    with col2:
        # CORRECTED: Uniform heading style, black text, single line, shortened date
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="metric-label">Forecast Period</div>
            <div class="metric-value">Nov '25 - Jan '26</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        strong_trends = forecast_df[forecast_df['trend_strength'] == 'strong']['ingredient'].nunique()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Strong Trends</div><div class="metric-value">{strong_trends}</div></div>', unsafe_allow_html=True)
    
    with col4:
        critical_reorders = data['reorder_alerts'][
            data['reorder_alerts']['forecasted_alert'].str.contains('Critical|Urgent', na=False)
        ].shape[0]
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Critical Reorders</div><div class="metric-value">{critical_reorders}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ingredient selector
    st.markdown("### Select Ingredient to Analyze")
    ingredients = sorted(historical_df['ingredient'].unique())
    selected = st.selectbox("Choose an ingredient:", ingredients, label_visibility="collapsed")
    
    # Get unit for selected ingredient
    selected_unit = get_unit_for_ingredient(selected, data)
    
    # Filter data for selected ingredient
    ingredient_historical = historical_df[historical_df['ingredient'] == selected].sort_values('period')
    ingredient_forecast = forecast_df[forecast_df['ingredient'] == selected].sort_values('period')
    
    # Metrics for selected ingredient - UNITS INLINE
    col1, col2, col3, col4 = st.columns(4)
    
    historical_only = ingredient_historical[ingredient_historical['data_type'] == 'historical']
    
    with col1:
        avg_usage = historical_only['value'].mean()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Historical Avg</div><div class="metric-value">{avg_usage:,.1f} {selected_unit}</div></div>', unsafe_allow_html=True)
    
    with col2:
        if not ingredient_forecast.empty:
            forecast_avg = ingredient_forecast['forecasted_usage'].mean()
            st.markdown(f'<div style="text-align:center;"><div class="metric-label">Forecast Avg</div><div class="metric-value">{forecast_avg:,.1f} {selected_unit}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center;"><div class="metric-label">Forecast Avg</div><div class="metric-value">N/A</div></div>', unsafe_allow_html=True)
    
    with col3:
        max_usage = historical_only['value'].max()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Peak Usage</div><div class="metric-value">{max_usage:,.1f} {selected_unit}</div></div>', unsafe_allow_html=True)
    
    with col4:
        std_usage = historical_only['value'].std()
        st.markdown(f'<div style="text-align:center;"><div class="metric-label">Volatility</div><div class="metric-value">{std_usage:,.1f} {selected_unit}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Time series with historical + forecast
    st.markdown(f"### 📈 Usage Trend & 3-Month Forecast: {selected.title()}")
    
    fig = go.Figure()
    
    # Historical data
    hist_data = ingredient_historical[ingredient_historical['data_type'] == 'historical']
    fig.add_trace(go.Scatter(
        x=hist_data['period'],
        y=hist_data['value'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    
    # Forecast data
    if not ingredient_forecast.empty:
        fig.add_trace(go.Scatter(
            x=ingredient_forecast['period'],
            y=ingredient_forecast['forecasted_usage'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond')
        ))
    
    # Average line
    fig.add_hline(
        y=avg_usage,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Historical Avg: {avg_usage:,.1f} {selected_unit}",
        annotation_position="top right"
    )
    
    # Trend line
    if len(historical_only) > 2:
        z = np.polyfit(range(len(historical_only)), historical_only['value'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=historical_only['period'],
            y=p(range(len(historical_only))),
            mode='lines',
            name='Trend',
            line=dict(color='green', width=2, dash='dash')
        ))
    
    fig.update_layout(
        height=450,
        hovermode='x unified',
        yaxis_title=f"Usage ({selected_unit})",
        xaxis_title="Period",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast details - WITH UNITS
    if not ingredient_forecast.empty:
        st.markdown("### 📊 Detailed Forecast")
        
        col1, col2 = st.columns(2)
        
        with col1:
            forecast_detail = ingredient_forecast[['period', 'forecasted_usage', 'trend_strength', 'r_squared']].copy()
            forecast_detail['Month'] = forecast_detail['period'].dt.strftime('%B %Y')
            forecast_detail[f'Forecasted Usage ({selected_unit})'] = forecast_detail['forecasted_usage'].apply(lambda x: f"{x:,.1f}")
            forecast_detail['Trend Strength'] = forecast_detail['trend_strength'].str.capitalize()
            forecast_detail['R-Squared'] = forecast_detail['r_squared'].round(4)
            
            forecast_detail = forecast_detail[['Month', f'Forecasted Usage ({selected_unit})', 'Trend Strength', 'R-Squared']]
            
            st.dataframe(forecast_detail, use_container_width=True, hide_index=True)
        
        with col2:
            # Get summary for this ingredient
            if selected in forecast_summary_df['ingredient'].values:
                summary = forecast_summary_df[forecast_summary_df['ingredient'] == selected].iloc[0]
                
                st.markdown("**Forecast Summary:**")
                st.write(f"- **Trend Strength:** {summary['trend_strength'].capitalize()}")
                st.write(f"- **R-Squared:** {summary['r_squared']:.4f}")
                st.write(f"- **Change from Historical:** {summary['pct_change_from_historical']:.1f}%")
                
                if summary['pct_change_from_historical'] > 0:
                    st.success(f"📈 Expected to increase by {summary['pct_change_from_historical']:.1f}%")
                else:
                    st.warning(f"📉 Expected to decrease by {abs(summary['pct_change_from_historical']):.1f}%")
    
    st.markdown("---")
    
    # Seasonal Insights - WITH UNITS INLINE
    if selected in seasonal_df['ingredient'].values:
        st.markdown("### 📅 Seasonal Usage Patterns")
        
        seasonal_info = seasonal_df[seasonal_df['ingredient'] == selected].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Peak Month:** {seasonal_info['peak_month']}\n\n**Usage:** {seasonal_info['peak_usage']:,.0f} {selected_unit}")
        
        with col2:
            st.info(f"**Low Month:** {seasonal_info['low_month']}\n\n**Usage:** {seasonal_info['low_usage']:,.0f} {selected_unit}")
        
        with col3:
            st.info(f"**Seasonal Variation:** {seasonal_info['seasonal_variation_%']:.1f}%\n\n**Volatility:** {seasonal_info['volatility']:,.1f} {selected_unit}")
    
    st.markdown("---")
    
    # Comparison heatmap
    st.markdown("### 🔥 All Ingredients Historical Usage Comparison")
    st.caption("Note: Different ingredients may have different units of measurement (g, count, units, pcs)")
    
    # Create pivot for heatmap
    pivot_data = historical_df[historical_df['data_type'] == 'historical'].pivot(
        index='ingredient',
        columns='period',
        values='value'
    )
    
    fig = px.imshow(
        pivot_data,
        x=[d.strftime('%b %Y') for d in pivot_data.columns],
        y=pivot_data.index,
        color_continuous_scale='YlOrRd',
        aspect='auto',
        labels=dict(x="Month", y="Ingredient", color="Usage")
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # AI INSIGHTS SECTION
    # ========================================================================
    st.markdown("### 🤖 AI-Powered Insights")
    
    st.info("💡 Generate personalized, actionable insights using Claude AI based on the forecasting data and trends for this ingredient.")
    
    # Prepare context data for AI - WITH UNITS
    context_summary = f"""
**Restaurant:** Mai Shan Yun

**Current Ingredient Being Analyzed:** {selected}
**Unit of Measurement:** {selected_unit}

**Historical Data Summary:**
- Average Monthly Usage: {avg_usage:,.1f} {selected_unit}
- Peak Usage: {max_usage:,.1f} {selected_unit}
- Volatility (Standard Deviation): {std_usage:,.1f} {selected_unit}

**Forecast Summary:**
"""
    
    if not ingredient_forecast.empty and selected in forecast_summary_df['ingredient'].values:
        summary = forecast_summary_df[forecast_summary_df['ingredient'] == selected].iloc[0]
        context_summary += f"""
- Forecasted Average Usage (Next 3 Months): {summary['avg_forecasted_usage']:,.1f} {selected_unit}
- Trend Strength: {summary['trend_strength'].capitalize()}
- Expected Change from Historical: {summary['pct_change_from_historical']:.1f}%
"""
    
    if selected in seasonal_df['ingredient'].values:
        seasonal_info = seasonal_df[seasonal_df['ingredient'] == selected].iloc[0]
        context_summary += f"""
**Seasonal Patterns:**
- Peak Month: {seasonal_info['peak_month']} ({seasonal_info['peak_usage']:,.0f} {selected_unit})
- Low Month: {seasonal_info['low_month']} ({seasonal_info['low_usage']:,.0f} {selected_unit})
- Seasonal Variation: {seasonal_info['seasonal_variation_%']:.1f}%
"""
    
    # Reorder alert info
    if selected in data['reorder_alerts']['ingredient'].values:
        reorder_info = data['reorder_alerts'][data['reorder_alerts']['ingredient'] == selected].iloc[0]
        context_summary += f"""
**Inventory Status:**
- Current Alert: {reorder_info['forecasted_alert']}
- Days Until Depletion (Forecasted): {reorder_info['forecasted_days_until_depletion']:.1f} days
- Weekly Usage (Forecasted): {reorder_info['forecasted_weekly_usage']:,.1f} {selected_unit}
"""
    
    # Cost impact
    if selected in cost_df['ingredient'].values:
        cost_info = cost_df[cost_df['ingredient'] == selected].iloc[0]
        context_summary += f"""
**Shipment Requirements (Based on Forecast):**
- Average Monthly Forecast: {cost_info['avg_monthly_forecast']:,.1f} {selected_unit}
- Shipments Needed Per Month: {cost_info['shipments_needed_per_month']:.0f}
- Delivery Frequency: {cost_info['frequency']}
"""
    
    # Generate insights button
    if st.button("🚀 Generate AI Insights", type="primary"):
        with st.spinner("🤖 Claude AI is analyzing your data..."):
            
            user_prompt = f"""Generate comprehensive, business-focused insights for {selected} ingredient (measured in {selected_unit}) at Mai Shan Yun restaurant. 
            
The restaurant manager needs to understand:
1. What the forecast data indicates about future demand
2. Whether ordering patterns should be adjusted
3. Key risks or opportunities to be aware of
4. Specific, actionable recommendations for the next month

Please use clear, professional language that is accessible to non-technical stakeholders."""
            
            ai_response = call_claude_agent(user_prompt, context_summary)
            
            # Display AI response
            st.markdown("#### 💡 AI-Generated Insights")
            
            st.markdown(f"""
<div class="insight-box">
{ai_response}
</div>
""", unsafe_allow_html=True)
            
            # Download option
            st.download_button(
                label="📥 Download Complete Insights Report",
                data=f"AI Insights Report for {selected}\nGenerated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n{'='*70}\n\n{context_summary}\n\n{'='*70}\n\nAI INSIGHTS:\n\n{ai_response}",
                file_name=f"insights_{selected.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Show context data used
    with st.expander("📋 View Data Context Provided to AI"):
        st.text(context_summary)

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p><strong>Mai Shan Yun Analytics Dashboard</strong> | Powered by Streamlit & Claude AI</p>
        <p>Last Updated: {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
""", unsafe_allow_html=True)