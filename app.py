import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cricket Analytics", layout="wide")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("🏏 Cricket Analytics")
menu = st.sidebar.radio("Navigation", ["Home", "Match Analysis", "Player Insights", "Team Comparison"])

# ---------------------------
# HOME
# ---------------------------
if menu == "Home":
    st.title("🏏 Cricket Analytics Dashboard")
    st.write("""
    Welcome to the Cricket Analytics site — built with Streamlit.  
    Upload cricket data (Cricsheet, ESPNcricinfo, CSV files) and generate insights instantly.
    """)
    st.image("https://images.pexels.com/photos/269948/pexels-photo-269948.jpeg")

# ---------------------------
# MATCH ANALYSIS
# ---------------------------
elif menu == "Match Analysis":
    st.title("📊 Match Analysis")

    uploaded = st.file_uploader("Upload match data (CSV / Cricsheet JSON)", type=["csv", "json"])

    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_json(uploaded)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # Basic Stats
        st.subheader("Basic Match Stats")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Balls", len(df))
        col2.metric("Total Runs", df["runs"].sum() if "runs" in df else "-")
        col3.metric("Wickets", df["wicket"].sum() if "wicket" in df else "-")

        # Runs per over
        st.subheader("Runs per Over")
        if "over" in df and "runs" in df:
            runs_over = df.groupby("over")["runs"].sum()

            fig, ax = plt.subplots()
            ax.plot(runs_over.index, runs_over.values)
            ax.set_xlabel("Over")
            ax.set_ylabel("Runs")
            ax.set_title("Runs per Over")
            st.pyplot(fig)

        # Wickets timeline
        st.subheader("Wickets Timeline")
        if "ball" in df and "wicket" in df:
            fig2, ax2 = plt.subplots()
            ax2.scatter(df["ball"], df["wicket"])
            ax2.set_xlabel("Ball Number")
            ax2.set_ylabel("Wicket Event")
            ax2.set_title("Wicket Timeline")
            st.pyplot(fig2)

# ---------------------------
# PLAYER INSIGHTS
# ---------------------------
elif menu == "Player Insights":
    st.title("👤 Player Performance Insights")

    uploaded = st.file_uploader("Upload player stats (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())

        players = df["player"].unique()
        chosen = st.selectbox("Select Player", players)

        pdf = df[df["player"] == chosen]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Runs", pdf["runs"].sum())

        with col2:
            st.metric("Strike Rate", round((pdf["runs"].sum() / len(pdf)) * 100, 2))

        # Line chart: runs progression
        st.subheader("Runs Progression")
        fig, ax = plt.subplots()
        ax.plot(pdf["ball"], pdf["runs"].cumsum())
        ax.set_xlabel("Ball")
        ax.set_ylabel("Cumulative Runs")
        st.pyplot(fig)

# ---------------------------
# TEAM COMPARISON
# ---------------------------
elif menu == "Team Comparison":
    st.title("⚔️ Team Comparison")

    uploaded = st.file_uploader("Upload team-wise stats (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())

        teams = df["team"].unique()

        t1 = st.selectbox("Team 1", teams)
        t2 = st.selectbox("Team 2", teams)

        df1 = df[df["team"] == t1]
        df2 = df[df["team"] == t2]

        col1, col2 = st.columns(2)
        col1.metric(f"{t1} Total Runs", df1["runs"].sum())
        col2.metric(f"{t2} Total Runs", df2["runs"].sum())

        # Compare run rate
        st.subheader("Run Rate Comparison")
        fig, ax = plt.subplots()
        ax.plot(df1["over"], df1["runs"], label=t1)
        ax.plot(df2["over"], df2["runs"], label=t2)
        ax.set_xlabel("Over")
        ax.set_ylabel("Runs")
        ax.legend()
        st.pyplot(fig)

