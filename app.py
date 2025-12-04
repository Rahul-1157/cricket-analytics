import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Cricket Analytics Hub", layout="wide")

st.title("🏏 Cricket Analytics Hub – Streamlit (Upgraded Version)")
st.write("Upload cricket datasets → explore visuals → auto insights → generate summaries.")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("📂 Upload Cricket Data")
data_file = st.sidebar.file_uploader("Upload CSV (Cricsheet ball-by-ball, match stats, player stats)")

page = st.sidebar.radio("Navigation", ["Dataset Preview", "Visualizations", "Insights", "AI Summaries"])

if not data_file:
    st.info("Upload a CSV file to begin.")
    st.stop()

# Load dataset
try:
    df = pd.read_csv(data_file)
except:
    st.error("Invalid CSV format. Please upload a valid file.")
    st.stop()

num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

# ---------------------------
# PAGE 1 – Dataset Preview
# ---------------------------
if page == "Dataset Preview":
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("🔍 Column Information")
    st.write(df.dtypes)

# ---------------------------
# PAGE 2 – Visualizations
# ---------------------------
elif page == "Visualizations":
    st.subheader("📈 Build Visualizations")

    vis_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])
    x_axis = st.selectbox("X-axis", options=df.columns)

    if vis_type == "Histogram":
        y_axis = None
    else:
        y_axis = st.selectbox("Y-axis", options=num_cols)

    if st.button("Generate Chart"):
        if vis_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart")
        elif vis_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        elif vis_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
        elif vis_type == "Histogram":
            fig = px.histogram(df, x=x_axis, title="Histogram")

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# PAGE 3 – Insights
# ---------------------------
elif page == "Insights":
    st.subheader("🧠 Auto Statistical Insights")
    feature = st.selectbox("Select a Feature", df.columns)

    st.write("### Summary Stats")
    st.write(df[feature].describe())

    st.write("### Unique Values")
    st.write(df[feature].unique()[:25])

# ---------------------------
# PAGE 4 – AI Summaries (Placeholder)
# ---------------------------
elif page == "AI Summaries":
    st.subheader("🤖 AI Match Summary Generator")
    summary_type = st.selectbox("Summary Type", [
        "Match Story",
        "Batting Summary",
        "Bowling Summary",
        "Partnership Insights",
        "Player Impact Report"
    ])

    st.write("### Generated Summary")
    st.write("(AI summary placeholder — connect OpenAI or Gemini API here)")
