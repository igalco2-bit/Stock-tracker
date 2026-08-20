import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="תיק המניות שלי", page_icon="📈", layout="centered")

st.title("📈 מעקב תיק מניות אוטומטי")

# טבלת נתונים בזיכרון הדינמי של האפליקציה
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = [
        {"name": "שופרסל", "ticker": "SAE.TA", "buy_price": 45.13}
    ]

with st.form("add_stock_form"):
    st.subheader("הוספת מניה חדשה")
    stock_name = st.text_input("שם המניה (למשל: שופרסל)")
    ticker_symbol = st.text_input("סימול מניה ב-Yahoo Finance (למשל: SAE.TA)")
    buy_price = st.number_input("שער קניה", min_value=0.0, step=0.01)
    
    submitted = st.form_submit_button("הוסף לתיק")
    if submitted and stock_name and ticker_symbol:
        st.session_state.portfolio.append({
            "name": stock_name, 
            "ticker": ticker_symbol, 
            "buy_price": buy_price
        })
        st.success( נוספה בהצלחה!)

st.subheader("התיק שלי")

if st.session_state.portfolio:
    data = []
    for item in st.session_state.portfolio:
        try:
            # שליפה אוטומטית של השער הנוכחי מהאינטרנט
            stock_data = yf.Ticker(item["ticker"])
            current_price = stock_data.history(period="1d")['Close'].iloc[-1]
        except:
            current_price = item["buy_price"] # גיבוי במקרה של תקלת תקשורת
            
        profit_loss_pct = ((current_price - item["buy_price"]) / item["buy_price"]) * 100
        
        data.append({
            "שם מניה": item["name"],
            "שער קניה": f"{item['buy_price']:.2f} ₪",
            "שער נוכחי": f"{current_price:.2f} ₪",
            "רווח/הפסד": f"{profit_loss_pct:+.2f}%"
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("התיק ריק. הוסף מניות באמצעות הטופס למעלה.")
