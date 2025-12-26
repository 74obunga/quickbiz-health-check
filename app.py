import streamlit as st
from logic import business_health
from report import generate_report
import pandas as pd


st.set_page_config(page_title="QuickBiz Health Check", page_icon="📊")

st.title("📊 QuickBiz Health Check")
st.caption("Instant cash runway & risk check for small businesses")

st.markdown("### 📂 Upload Transactions (Optional)")
uploaded_file = st.file_uploader(
    "Upload a CSV with an 'amount' column",
     type=["csv"]
)    
auto_revenue = 0.0
auto_expenses = 0.0
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "amount" in df.columns:
        auto_revenue = df[df["amount"] > 0]["amount"].sum()
        auto_expenses = abs(df[df["amount"] < 0]["amount"].sum())

        st.success("Transactions processed successfully")
    else:
        st.error("CSV must contain an 'amount' column")    

revenue = st.number_input(
    "Monthly Revenue",
    min_value=0.0,
    value=float(auto_revenue)
)
expenses = st.number_input(
    "Monthly Expenses",
    min_value=0.0,
    value=float(auto_expenses)
)
cash = st.number_input("Cash Balance", min_value=0.0)
debtors = st.number_input("Debtors (Money owed to you)", min_value=0.0)
creditors = st.number_input("Creditors (Money you owe)", min_value=0.0)

if st.button("Analyze Business"):
    result = business_health(revenue, expenses, cash, debtors, creditors)

    st.subheader("📈 Business Snapshot")
    
    st.metric("Profit", f"{result['profit']}")
    st.metric("Profit Margin (%)", f"{result['profit_margin']}")
    st.metric("Cash Runway (months)", f"{result['runway']}")
    st.metric("Risk Level", result["risk"])

    st.info(result["advice"])

    html_report = generate_report(result)

    st.download_button(
        label="📥 Download Business Report",
        data=html_report,
        file_name="QuickBiz_Health_Report.html",
        mime="text/html"
    )

    st.markdown("---")
    st.markdown("### 💳 Pricing")
    st.markdown(
        "This report normally costs **KES 500 ($4)**. "
        "Early users can generate reports **free today** while we test the tool."
    ) 

    st.markdown("### 📲 Want monthly tracking?")
    st.markdown(
        "Get ongoing business insights and reminders via WhatsApp. "
        "Message **'BIZ CHECK'** to +254711179773" 
    )      
