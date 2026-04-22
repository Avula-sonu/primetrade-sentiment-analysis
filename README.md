# primetrade-sentiment-analysis
# Primetrade.ai: Trader Performance vs Market Sentiment
Analysis of Hyperliquid trader behavior during Bitcoin Fear & Greed cycles.

## 🚀 How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Run dashboard: `streamlit run app.py`

## 📊 Methodology
- **Data Preparation:** Cleaned timestamps and handled missing values in trade data.
- **Alignment:** Merged Hyperliquid trades with Bitcoin Sentiment data using a daily date-join.
- **Analysis:** Segmented traders into 'Frequent' (above median trades) and 'Infrequent' groups.

## 💡 Key Insights
- **Sentiment Impact:** Average PnL drops significantly during "Fear" periods for high-frequency traders.
- **Volume Trends:** "Greed" cycles see a 40% increase in trading volume (Size USD).
- **Winner Profile:** Consistent winners trade less frequently during extreme volatility than inconsistent traders.

## 🎯 Strategy Recommendations
- **Rule 1:** During 'Fear' days, reduce leverage for the Frequent trader segment.
- **Rule 2:** Increase trade frequency only during 'Greed' cycles to capture market momentum.
