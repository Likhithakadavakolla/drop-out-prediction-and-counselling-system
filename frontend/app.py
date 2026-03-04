import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("🎓 AI-based Student Dropout Prediction Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/student_data.csv")
st.success("Student dataset loaded successfully")

st.subheader("📄 Student Data")
st.dataframe(df, width="stretch")

# ---------------- PREDICTION ----------------
def predict_risk(row):
    if row["attendance"] < 40 or row["marks"] < 35 or row["attempts"] >= 3:
        return "HIGH RISK"
    elif row["attendance"] < 60 or row["marks"] < 50:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"

if st.button("Predict for All Students"):
    df["risk_level"] = df.apply(predict_risk, axis=1)

    def color_risk(val):
        if val == "HIGH RISK":
            return "background-color:red;color:white"
        elif val == "MEDIUM RISK":
            return "background-color:orange;color:black"
        else:
            return "background-color:green;color:white"

    st.subheader("📊 Risk Prediction")
    st.dataframe(df.style.applymap(color_risk, subset=["risk_level"]), width="stretch")

    st.subheader("📧 Send Alerts")

    for _, row in df.iterrows():
        if row["risk_level"] == "HIGH RISK":
            if st.button(f"Notify Student {row['student_id']}"):
                payload = {
                    "student_id": int(row["student_id"]),
                    "risk_level": row["risk_level"],
                    "guardian_email": row["guardian_email"],
                    "mentor_email": row["mentor_email"]
                }

                r = requests.post("http://127.0.0.1:8000/notify", json=payload)

                if r.status_code == 200:
                    st.success(f"Emails sent for Student {row['student_id']}")
                else:
                    st.error("Failed to send email")
