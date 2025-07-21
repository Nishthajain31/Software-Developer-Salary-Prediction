import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.set_page_config(page_title="Explore Salaries", layout="centered")

    # Same gradient and layout as predict_page.py
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

            .stPlotlyChart, .stPyplotChart, .stMarkdown {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    st.markdown("## 📊 Explore Software Engineer Salaries")
    st.write("### Based on Stack Overflow Developer Survey 2020")

    st.write("#### Number of Responses by Country")
    country_data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(country_data, labels=country_data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    st.write("#### 💸 Mean Salary by Country")
    country_salary = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(country_salary)

    st.write("#### 🧑‍💻 Mean Salary by Years of Experience")
    experience_salary = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    st.line_chart(experience_salary)

    st.markdown("</div>", unsafe_allow_html=True)
