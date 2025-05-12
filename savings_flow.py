import streamlit as st
import json
import re
import requests

SAVINGS_PREDICTOR_URL = "http://13.234.57.143:7860/api/v1/run/43c93e1b-54c4-4852-ad91-0451bcf9a509"

def savings_goal_page():
    st.subheader("💰 Savings Goals")

    # Default landing text
    st.markdown("""
        Do you have any personal savings goals? We can help you analyze your spending patterns and suggest improvements.

        Type in the chat window below.

        **Example:**  
        `I want to save Rs. 5,00,000 in the next 3 years.`
    """)

    # Initialize form visibility flag in session state
    if "show_spending_form" not in st.session_state:
        st.session_state.show_spending_form = False

    # Detect savings amount from assistant messages if not already set
    if "savings_amount" not in st.session_state:
        for message in reversed(st.session_state.get("messages", [])):
            if message["role"] == "assistant":
                match = re.search(r"your desired monthly savings amount is\s+Rs\.?\s?(\d+(\.\d+)?)", message["content"], re.IGNORECASE)
                if match:
                    st.session_state.savings_amount = float(match.group(1))
                    break  # No need to rerun — just extract and move on

    # Button to show the form
    if st.button("🔍 Analyze My Spending Patterns"):
        st.session_state.show_spending_form = True

    # Show the form if user clicked the button
    if st.session_state.show_spending_form:
        if "savings_amount" not in st.session_state:
            st.info("Please tell me your savings goal in the chat window first so I can personalize the form.")
            return

        monthly_savings = st.session_state.savings_amount

        st.markdown(f"💡 Your desired monthly savings amount is Rs. {monthly_savings:.2f}.")
        st.markdown("Please fill in the details below for analysis of your demographics and spending patterns:")

        with st.form("savings_form"):
            income = st.text_input("Monthly Income", "100000")
            age = st.text_input("Age", "25")
            dependents = st.text_input("Dependents", "1")
            occupation = st.selectbox("Occupation", ["Salaried", "Self_Employed", "Other"], index=0)
            city_tier = st.selectbox("City Tier", ["Tier_1", "Tier_2", "Tier_3"], index=0)
            rent = st.text_input("Monthly Rent", "10000")
            loan_repayment = st.text_input("Loan Repayment", "0")
            insurance = st.text_input("Insurance Premium", "10000")
            other_exp = st.text_input("Other Expenditures", "10000")
            desired_savings = st.text_input("Desired Monthly Savings", f"{monthly_savings:.2f}")

            submit_button = st.form_submit_button("Submit")

        if submit_button:
            payload = {
                "input_value": json.dumps({
                    "savings": {
                        "Income": income,
                        "Age": age,
                        "Dependents": dependents,
                        "Occupation": occupation,
                        "City_Tier": city_tier,
                        "Rent": rent,
                        "Loan_Repayment": loan_repayment,
                        "Insurance": insurance,
                        "total_expenditure_others": other_exp,
                        "Desired_Savings": desired_savings
                    }
                }),
                "input_type": "chat",
                "output_type": "chat"
            }

            try:
                response = requests.post(SAVINGS_PREDICTOR_URL, json=payload)
                if response.ok:
                    result = response.json()
                    prediction = result["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    st.success(f"💡 {prediction}")
                else:
                    st.error("❌ Failed to get prediction from LangFlow.")
            except Exception as e:
                st.error(f"🚨 Error: {e}")
