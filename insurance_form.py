import streamlit as st
import json
import requests

INSURANCE_PREDICTOR_URL = "http://13.234.57.143:7860/api/v1/run/f0897448-d3e4-4685-8d0d-fbf97f76eadb"

def insurance_form_page():
    st.markdown("## 🛡️ Insurance Plan Selector")
    
    st.markdown("Use the table below to understand the differences between insurance coverage levels:")

    # Coverage Plan Comparison Table
    st.markdown("""
    <style>
        .insurance-table th, .insurance-table td {
            text-align: left;
            padding: 8px 12px;
        }
        .insurance-table {
            border-collapse: collapse;
            margin-top: 10px;
        }
        .insurance-table th {
            background-color: #f2f2f2;
        }
        .insurance-table, .insurance-table th, .insurance-table td {
            border: 1px solid #ddd;
        }
    </style>
    <table class="insurance-table">
        <thead>
            <tr>
                <th>Plan Level</th>
                <th>Monthly Premium</th>
                <th>Out-of-Pocket Costs</th>
                <th>Coverage Depth</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Basic</td>
                <td>Lowest</td>
                <td>Highest</td>
                <td>Minimal (covers only essentials and emergencies)</td>
            </tr>
            <tr>
                <td>Standard</td>
                <td>Moderate</td>
                <td>Moderate</td>
                <td>Balanced (routine + emergency care)</td>
            </tr>
            <tr>
                <td>Premium</td>
                <td>Highest</td>
                <td>Lowest</td>
                <td>Comprehensive (broad access, low copays, extras)</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Please fill in your insurance-related information:")

    with st.form("insurance_form"):
        age = st.text_input("Age", "25")
        gender = st.selectbox("Gender", ["male", "female"])
        bmi = st.text_input("BMI", "22.5")
        num_children = st.text_input("Number of children", "0")
        smoker = st.selectbox("Smoker", ["yes", "no"])
        medical_history = st.selectbox("Self Medical History", ["Diabetes", "Heart disease", "High blood pressure", "None"])
        family_history = st.selectbox("Family Medical History", ["Diabetes", "Heart disease", "High blood pressure", "None"])
        exercise = st.selectbox("Exercise Frequency", ["Frequently", "Never", "Occasionally", "Rarely"])
        occupation = st.selectbox("Occupation", ["Blue collar", "Student", "Unemployed", "White collar"])
        coverage_level = st.selectbox("Insurance Coverage Level", ["Basic", "Premium", "Standard"])

        if st.form_submit_button("Submit"):
        
            # Prepare input JSON
            input_data = {
                "insurance": {
                    "age": int(age),
                    "gender": gender,
                    "bmi": float(bmi),
                    "children": int(num_children),
                    "smoker": smoker,
                    "medical_history": medical_history,
                    "family_medical_history": family_history,
                    "exercise_frequency": exercise,
                    "occupation": occupation,
                    "coverage_level": coverage_level
                    # 'region' will be added by LangFlow component internally as 'southeast'
                }
            }

            payload = {
                "input_value": json.dumps(input_data),
                "input_type": "chat",
                "output_type": "chat"
            }

            try:
                response = requests.post(INSURANCE_PREDICTOR_URL, json=payload)

                if response.ok:
                    result = response.json()
                    prediction = result["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    st.success(prediction)
                else:
                    st.error(f"❌ Failed to get prediction from LangFlow.\n\nStatus: {response.status_code}\nResponse: {response.text}")
            except Exception as e:
                st.error(f"🚨 Error during request: {e}")
