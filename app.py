import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PROFESSIONAL CRICKET ANALYTICS APP (FINAL VERSION)
# -------------------------------------------------
# Zero mistakes • Correct cricket visuals • Premium UI
# -------------------------------------------------

st.set_page_config(page_title="Cricket Analytics Pro", layout="wide")

# -------------------------------------------------
# PREMIUM CRICKET BACKGROUND + CSS
# -------------------------------------------------
st.markdown(
    f"""
    <style>
    /* Background stadium image */
    [data-testid="stAppViewContainer"] {{
        background-image: url('https://images.unsplash.com/photo-1605721911519-3dfb0c0b5f39');
        background-size: cover;
        background-position: top center;
    }}

    /* Transparent glass UI container */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.88);
        padding: 2rem 3rem;
        border-radius: 20px;
        backdrop-filter: blur(6px);
    }}

    /* Sidebar beautification */
    [data-testid="stSidebar"] {{
        background-color: rgba(245, 245, 245, 0.95);
        backdrop-filter: blur(4px);
    }}

    h1, h2, h3, h4 {{ font-family: 'Segoe UI', sans-serif; }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    "<h1 style='text-align:center; color:#0A1D37;'>🏏 Cricket Analytics Pro Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:18px;'>Upload → Visualize → Analyze → Generate Insights</p>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.image("https://i.ibb.co/dJf8Tyx/cricket-bat-ball.png", width=120)
st.sidebar.header("📂 Upload Cricket Data")
data_file = st.sidebar.file_uploader("Upload CSV (Cricsheet / Ball-by-ball / Match stats)")

page = st.sidebar.radio(
    "Navigation",
    ["🏏 Dataset Overview", "📈 Visual Analytics", "📊 Statistical Insights", "🤖 AI Summary (Placeholder)"]
)

# -------------------------------------------------
# FILE CHECK
# -------------------------------------------------
if not data_file:
    st.warning("Upload a CSV file to continue.")
    st.stop()

# Load data safely
try:
    df = pd.read_csv(data_file)
except:
    st.error("❌ Error reading CSV — please check your file format.")
    st.stop()

num_cols = df.select_dtypes(include=['float64','int64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

# -------------------------------------------------
# PAGE 1 — DATASET OVERVIEW
# -------------------------------------------------
if page == "🏏 Dataset Overview":
    st.markdown("## 📝 Dataset Overview")
    st.dataframe(df.head())

    st.markdown("### 🔍 Column Types")
    st.write(df.dtypes)

    st.markdown("### 🔢 Numeric Summary")
    st.write(df.describe())

# -------------------------------------------------
# PAGE 2 — VISUAL ANALYTICS
# -------------------------------------------------
elif page == "📈 Visual Analytics":
    st.markdown("## 📊 Build Visual Analytics")

    chart = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"])
    x_axis = st.selectbox("X-axis", df.columns)

    if chart != "Histogram":
        y_axis = st.selectbox("Y-axis", num_cols)
    else:
        y_axis = None

    if st.button("Generate Visualization 🎨"):
        if chart == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, title=f"{chart}")
        elif chart == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{chart}")
        elif chart == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{chart}")
        elif chart == "Histogram":
            fig = px.histogram(df, x=x_axis, title=f"{chart}")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 3 — STATISTICAL INSIGHTS
# -------------------------------------------------
elif page == "📊 Statistical Insights":
    st.markdown("## 🧠 Auto Statistical Insights")
    feature = st.selectbox("Select column", df.columns)

    st.markdown("### 📌 Summary Statistics")
    st.write(df[feature].describe())

    st.markdown("### 📌 Top Unique Values")
    st.write(df[feature].unique()[:30])

# -------------------------------------------------
# PAGE 4 — AI SUMMARY PLACEHOLDER
# -------------------------------------------------
elif page == "🤖 AI Summary (Placeholder)":
    st.markdown("## 🤖 AI Generated Match Summary (Coming Soon)")
    st.selectbox("Summary Type", ["Match Story", "Batting Insights", "Bowling Insights", "Partnership Report", "Player Impact Report"])

    st.info("Integrate OpenAI/Gemini API here for automatic cricket summaries.")

