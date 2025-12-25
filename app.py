import streamlit as st
from logic import business_health
from report import generate_report

st.set_page_config(page_title="QuickBiz Health Check", page_icon="📊")

st.title("📊 QuickBiz Health Check")
st.caption("Know your business health in 2 minutes")

revenue = st.number_input("Monthly Revenue", min_value=0.0)
expenses = st.number_input("Monthly Expenses", min_value=0.0)
cash = st.number_input("Cash Balance", min_value=0.0)
debtors = st.number_input("Debtors (Money owed to you)", min_value=0.0)
creditors = st.number_input("Creditors (Money you owe)", min_value=0.0)

if st.button("Analyze Business"):
    result = business_health(revenue, expenses, cash, debtors, creditors)

    st.subheader("📈 Results")
    st.json(result)

    html_report = generate_report(result)

    st.download_button(
        label="📥 Download Business Report",
        data=html_report,
        file_name="QuickBiz_Health_Report.html",
        mime="text/html"
    )
