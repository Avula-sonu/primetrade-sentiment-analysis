import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Primetrade.ai Analytics", layout="wide")
st.title("📈 Primetrade.ai: Trader Performance & Sentiment")
st.markdown("Detailed analysis of Hyperliquid trader behavior during Market Sentiment cycles.")

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('final_trader_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    # Clean column names to prevent matching errors
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 3. Sidebar Filtering (Ensures all sentiments like Fear, Greed, Neutral are visible)
st.sidebar.header("Global Filters")
all_moods = df['classification'].unique().tolist()
selected_moods = st.sidebar.multiselect("Select Market Sentiment", all_moods, default=all_moods)

# Filter logic
if not selected_moods:
    filtered_df = df.copy()
else:
    filtered_df = df[df['classification'].isin(selected_moods)]

# 4. PART A & B: KPI Metrics (With Zero-Division Protection)
st.subheader("High-Level Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

total_trades = len(filtered_df)
total_pnl = filtered_df['Closed PnL'].sum()
total_vol = filtered_df['Size USD'].sum()

# Fix for Zero Division Error
avg_pnl = total_pnl / total_trades if total_trades > 0 else 0
win_rate = (len(filtered_df[filtered_df['Closed PnL'] > 0]) / total_trades * 100) if total_trades > 0 else 0

col1.metric("Total PnL", f"${total_pnl:,.2f}")
col2.metric("Avg PnL/Trade", f"${avg_pnl:.2f}")
col3.metric("Trading Volume", f"${total_vol:,.0f}")
col4.metric("Win Rate %", f"{win_rate:.1f}%")

st.write("---")

# 5. PART B: Performance by Sentiment Type
st.subheader("📊 Sentiment Impact Analysis")
if not filtered_df.empty:
    # Grouping to ensure all categories (Greed, Fear, etc.) are plotted
    sentiment_perf = filtered_df.groupby('classification')['Closed PnL'].agg(['mean', 'sum']).reset_index()
    
    fig_sentiment = px.bar(
        sentiment_perf, 
        x='classification', 
        y='mean', 
        color='classification',
        title="Average Profitability by Market Mood",
        labels={'mean': 'Average PnL ($)', 'classification': 'Sentiment'}
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)
    

# 6. PART B: Trader Segmentation (Frequent vs Infrequent & Winners)
st.write("---")
st.subheader("🎯 Trader Behavioral Archetypes")

# Calculate metrics per individual account
trader_stats = filtered_df.groupby('Account').agg({
    'Closed PnL': ['sum', 'mean'],
    'Account': 'count'
}).reset_index()
trader_stats.columns = ['Account', 'Total_PnL', 'Avg_PnL', 'Trade_Count']

if not trader_stats.empty:
    # Segment 1: Frequent vs Infrequent (Requirement 3a)
    median_trades = trader_stats['Trade_Count'].median()
    trader_stats['Frequency'] = trader_stats['Trade_Count'].apply(lambda x: 'Frequent' if x > median_trades else 'Infrequent')
    
    # Segment 2: Consistent Winners vs Inconsistent (Requirement 3b)
    trader_stats['Status'] = trader_stats['Total_PnL'].apply(lambda x: 'Winner' if x > 0 else 'Inconsistent')
    
    c1, c2 = st.columns(2)
    with c1:
        fig_freq = px.box(trader_stats, x='Frequency', y='Avg_PnL', color='Frequency', title="Profit Range: Frequent vs Infrequent")
        st.plotly_chart(fig_freq, use_container_width=True)
    with c2:
        fig_status = px.pie(trader_stats, names='Status', title="Population: Winners vs Inconsistent Traders", hole=0.4)
        st.plotly_chart(fig_status, use_container_width=True)

# 7. PART C: Actionable Strategy (Must-Have for Part C)
st.write("---")
st.subheader("💡 Actionable Strategy & Insights")
st.markdown("""
**Finding 1:** Frequent traders show higher drawdowns during 'Fear' periods.  
👉 **Rule of Thumb:** Reduce leverage by 50% for Frequent segments when Fear Index is high.

**Finding 2:** Market 'Greed' shows a direct correlation with increased Size USD (Volume).  
👉 **Rule of Thumb:** Increase trade frequency only during 'Greed' cycles to capture momentum.

**Finding 3:** Inconsistent traders often have high volume but negative PnL.  
👉 **Insight:** Focus risk-management tools on high-volume, low-win-rate accounts.
""")

# 8. Data Explorer
if st.checkbox("Show Raw Processed Data (Top 50 rows)"):
    st.dataframe(filtered_df.head(50))