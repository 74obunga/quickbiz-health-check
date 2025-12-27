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
if uploaded_file is None:
    st.markdown("### ✍️ Manual Financial Inputs")

    cash = st.number_input("Cash Balance", min_value=0.0)
    debtors = st.number_input("Debtors (Money owed to you)", min_value=0.0)
    creditors = st.number_input("Creditors (Money you owe)", min_value=0.0)

    auto_revenue = 0
    auto_expenses = creditors  # fallback for runway
else:
    df = pd.read_csv(uploaded_file)

    if "amount" in df.columns:
        auto_revenue = df[df["amount"] > 0]["amount"].sum()
        auto_expenses = abs(df[df["amount"] < 0]["amount"].sum())

        if uploaded_file is not None:
            cash_balance = auto_revenue - auto_expenses
            st.metric("Cash Balance", f"KES {cash_balance:,.2f}")
        else:
            cash_balance = st.number_input("Cash Balance", min_value=0.0) 
        debtors = 0
        creditors = 0       
        

        st.success(
            f"Processed {len(df)} transactions | "
            f"Inflow: KES {auto_revenue:,.0f} | "
            f"Outflow: KES {auto_expenses:,.0f}"
        ) 
        st.markdown("#### 📊 Transaction Summary")
        st.write(f"Total transactions: {len(df)}")
        st.write(f"Total inflow: KES {auto_revenue:,.2f}")
        st.write(f"Total outflow: KES {auto_expenses:,.2f}")
        # Cash runway

        st.markdown("### 🛣️ Cash Runway")

        if auto_expenses > 0:
            runway_months = cash_balance / auto_expenses
            st.metric("Cash Runway (months)", f"{runway_months:.1f}")

            if runway_months < 3:
                st.error("🔴 High risk: Less than 3 months of cash left.")
            elif runway_months < 6: 
                st.warning("🟡 Medium risk: Consider building a cash buffer.") 
            else:
                st.success("🟢 Low risk: Cash position looks healthy.")  
        else:
            st.success("🟢 No expenses detected — runway is stable.")   

        st.progress(min(runway_months / 12, 1.0))
        st.caption("Runway compared to a 12-month safety benchmark")     


        
    else:
        st.error("CSV must contain an 'amount' column")  

if uploaded_file is None:
    st.info("Upload a CSV to see transaction analysis.")



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
