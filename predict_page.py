import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.set_page_config(page_title="Dev Salary Predictor", layout="centered")

    # Gradient and style
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

            html, body, [class*="css"]  {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #ffffff 0%, #ffe1e1 40%, #ffd4ae 100%);
                color: #333333;
            }

            .main-card {
                background: rgba(255, 255, 255, 0.75);
                padding: 2rem 3rem;
                border-radius: 20px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
                margin-top: 3rem;
            }

            .stButton > button {
                background-color: #ff6f61;
                color: white;
                border: none;
                padding: 0.6rem 1.3rem;
                font-size: 1rem;
                font-weight: 600;
                border-radius: 8px;
                transition: background 0.3s ease;
            }

            .stButton > button:hover {
                background-color: #e6574c;
            }

            .stSlider > div {{
                color: #333333;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    st.markdown("## ✨ Software Developer Salary Prediction")
    st.write("### Fill in your details to get an estimated salary:")

    countries = (
        "United States", "India", "United Kingdom", "Germany", "Canada",
        "Brazil", "France", "Spain", "Australia", "Netherlands",
        "Poland", "Italy", "Russian Federation", "Sweden"
    )

    education = (
        "Less than a Bachelors", "Bachelor’s degree", "Master’s degree", "Post grad"
    )

    country = st.selectbox("🌍 Country", countries)
    education_level = st.selectbox("🎓 Education Level", education)
    experience = st.slider("💼 Years of Experience", 0, 50, 3)

    if st.button("🎯 Calculate Salary"):
        X = np.array([[country, education_level, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.success(f"💵 Estimated Salary: **${salary[0]:,.2f}**")

    st.markdown("</div>", unsafe_allow_html=True)
