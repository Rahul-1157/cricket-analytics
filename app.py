import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# THEME + CRICKET UI
# -------------------------------------------------
st.set_page_config(page_title="🏏 Cricket Analytics Hub", layout="wide")

# Background Image
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url('https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a');
    background-size: cover;
    background-position: center;
}}

[data-testid="stHeader"] {{
    background-color: rgba(0,0,0,0);
}}

.block-container {{
    background-color: rgba(255, 255, 255, 0.82);
    padding: 2rem 3rem;
    border-radius: 20px;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center; color:#1a1a1a;'>🏏 Cricket Analytics Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Upload cricket data → View stats → Build visuals → Generate insights</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://i.ibb.co/vqBRF4P/cricket-stumps.png", width=150)
st.sidebar.header("📂 Upload Cricket Data")
data_file = st.sidebar.file_uploader("Upload CSV (Cricsheet ball-by-ball / match stats)")

page = st.sidebar.radio("Navigation", ["🏏 Dataset Preview", "📈 Visualizations", "📊 Insights", "🤖 AI Summaries"])

# If file not uploaded
if not data_file:
    st.warning("Please upload a cricket dataset CSV to begin.")
    st.stop()

# Load data
try:
    df = pd.read_csv(data_file)
except:
    st.error("Invalid CSV — please upload a correct file.")
    st.stop()

num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

# -------------------------------------------------
# PAGE 1 – Dataset Preview
# -------------------------------------------------
if page == "🏏 Dataset Preview":
    st.markdown("### 📝 Dataset Quick Preview")
    st.dataframe(df.head())

    st.markdown("### 🔍 Column Information")
    st.write(df.dtypes)

# -------------------------------------------------
# PAGE 2 – Visualizations
# -------------------------------------------------
elif page == "📈 Visualizations":
    st.markdown("### 📊 Create Interactive Cricket Charts")
    vis_type = st.selectbox("Choose Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])
    x_axis = st.selectbox("Choose X-axis", options=df.columns)

    y_axis = None
    if vis_type != "Histogram":
        y_axis = st.selectbox("Choose Y-axis", options=num_cols)

    if st.button("Generate Chart 🎨"):
        if vis_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart")
        elif vis_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        elif vis_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
        elif vis_type == "Histogram":
            fig = px.histogram(df, x=x_axis, title="Histogram")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 3 – Insights
# -------------------------------------------------
elif page == "📊 Insights":
    st.markdown("### 🧠 Automatic Statistical Insights")
    feature = st.selectbox("Select a Feature", df.columns)

    st.markdown("#### 📌 Summary Stats")
    st.write(df[feature].describe())

    st.markdown("#### 📌 Top Unique Values")
    st.write(df[feature].unique()[:20])

# -------------------------------------------------
# PAGE 4 – AI Summaries (Placeholder)
# -------------------------------------------------
elif page == "🤖 AI Summaries":
    st.markdown("### 🤖 AI Match Summary Generator")
    summary_type = st.selectbox("Summary Type", [
        "Match Story",
        "Batting Summary",
        "Bowling Summary",
        "Partnership Insights",
        "Player Impact Report"
    ])
    st.markdown("#### 🏆 Generated Summary")
    st.info("AI summary placeholder — Connect OpenAI or Gemini API here.")
