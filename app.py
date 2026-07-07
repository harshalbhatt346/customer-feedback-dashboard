"""
Customer Feedback Dashboard
----------------------------
A Streamlit web app that performs sentiment analysis on customer feedback
using TextBlob and visualizes the results with Plotly charts.

Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from io import StringIO

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Feedback Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# SENTIMENT ANALYSIS HELPERS
# ----------------------------------------------------------------------------
def get_sentiment(text: str):
    """Run TextBlob sentiment analysis on a piece of text.

    Returns polarity (-1 to 1), subjectivity (0 to 1), and a label.
    """
    if not isinstance(text, str) or text.strip() == "":
        return 0.0, 0.0, "Neutral"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return round(polarity, 3), round(subjectivity, 3), label


@st.cache_data(show_spinner=False)
def analyze_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sentiment analysis to every feedback row and cache the result."""
    df = df.copy()
    results = df["feedback"].apply(get_sentiment)
    df["polarity"] = results.apply(lambda x: x[0])
    df["subjectivity"] = results.apply(lambda x: x[1])
    df["sentiment"] = results.apply(lambda x: x[2])
    return df


@st.cache_data(show_spinner=False)
def load_default_data() -> pd.DataFrame:
    df = pd.read_csv("data/customer_feedback.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    content = uploaded_file.getvalue().decode("utf-8")
    df = pd.read_csv(StringIO(content))
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


# ----------------------------------------------------------------------------
# SIDEBAR — DATA SOURCE & FILTERS
# ----------------------------------------------------------------------------
st.sidebar.title("📊 Dashboard Controls")

st.sidebar.subheader("1. Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload your own CSV (optional)",
    type=["csv"],
    help="CSV must contain a 'feedback' column. 'date', 'customer_name', "
         "'product', and 'rating' columns are optional but recommended.",
)

if uploaded_file is not None:
    raw_df = load_uploaded_data(uploaded_file)
    st.sidebar.success(f"Loaded {len(raw_df)} rows from uploaded file.")
else:
    raw_df = load_default_data()
    st.sidebar.info("Using built-in sample dataset (30 reviews).")

if "feedback" not in raw_df.columns:
    st.error(
        "The dataset must contain a column named 'feedback' with the "
        "customer review text. Please check your CSV and try again."
    )
    st.stop()

# Run sentiment analysis (cached)
df = analyze_dataframe(raw_df)

# --- Filters ---
st.sidebar.subheader("2. Filters")

if "product" in df.columns:
    products = ["All"] + sorted(df["product"].dropna().unique().tolist())
    selected_product = st.sidebar.selectbox("Product", products)
    if selected_product != "All":
        df = df[df["product"] == selected_product]

sentiments = ["All", "Positive", "Neutral", "Negative"]
selected_sentiment = st.sidebar.selectbox("Sentiment", sentiments)
if selected_sentiment != "All":
    df = df[df["sentiment"] == selected_sentiment]

if "date" in df.columns and df["date"].notna().any():
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input(
        "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)]

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit · TextBlob · Plotly")

# ----------------------------------------------------------------------------
# MAIN PAGE — HEADER & KPIs
# ----------------------------------------------------------------------------
st.title("📊 Customer Feedback Dashboard")
st.markdown(
    "Analyze customer sentiment at a glance using **TextBlob** NLP sentiment "
    "scoring and interactive **Plotly** visualizations."
)

if df.empty:
    st.warning("No feedback matches the current filters. Try adjusting them in the sidebar.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

total_feedback = len(df)
positive_pct = (df["sentiment"] == "Positive").mean() * 100
negative_pct = (df["sentiment"] == "Negative").mean() * 100
avg_polarity = df["polarity"].mean()

with col1:
    st.metric("Total Feedback", total_feedback)
with col2:
    st.metric("Positive %", f"{positive_pct:.1f}%")
with col3:
    st.metric("Negative %", f"{negative_pct:.1f}%")
with col4:
    st.metric("Avg. Sentiment Score", f"{avg_polarity:.3f}")

st.markdown("---")

# ----------------------------------------------------------------------------
# CHARTS ROW 1 — Sentiment distribution & rating comparison
# ----------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sentiment Distribution")
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    color_map = {"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"}
    fig_pie = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        color="sentiment",
        color_discrete_map=color_map,
        hole=0.45,
    )
    fig_pie.update_traces(textinfo="percent+label")
    fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    if "rating" in df.columns:
        st.subheader("Star Rating vs. Sentiment")
        fig_box = px.box(
            df,
            x="sentiment",
            y="rating",
            color="sentiment",
            color_discrete_map=color_map,
            points="all",
        )
        fig_box.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.subheader("Polarity Distribution")
        fig_hist = px.histogram(df, x="polarity", nbins=20, color_discrete_sequence=["#3498db"])
        fig_hist.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------------------------------------------------------------
# CHARTS ROW 2 — Trend over time & product breakdown
# ----------------------------------------------------------------------------
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    if "date" in df.columns and df["date"].notna().any():
        st.subheader("Sentiment Trend Over Time")
        trend_df = (
            df.groupby([pd.Grouper(key="date", freq="D"), "sentiment"])
            .size()
            .reset_index(name="count")
        )
        fig_trend = px.line(
            trend_df,
            x="date",
            y="count",
            color="sentiment",
            color_discrete_map=color_map,
            markers=True,
        )
        fig_trend.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.subheader("Subjectivity vs. Polarity")
        fig_scatter = px.scatter(
            df, x="polarity", y="subjectivity", color="sentiment",
            color_discrete_map=color_map, hover_data=["feedback"]
        )
        fig_scatter.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col4:
    if "product" in df.columns:
        st.subheader("Sentiment by Product")
        prod_sentiment = (
            df.groupby(["product", "sentiment"]).size().reset_index(name="count")
        )
        fig_bar = px.bar(
            prod_sentiment,
            x="product",
            y="count",
            color="sentiment",
            color_discrete_map=color_map,
            barmode="stack",
        )
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.subheader("Average Polarity")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_polarity,
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={"axis": {"range": [-1, 1]}},
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# WORD-LEVEL INSIGHT — Most polarized feedback
# ----------------------------------------------------------------------------
st.subheader("🔥 Most Positive & Most Negative Feedback")
insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("**Top 3 Most Positive**")
    top_pos = df.sort_values("polarity", ascending=False).head(3)
    for _, row in top_pos.iterrows():
        st.success(f"⭐ {row['polarity']:.2f} — {row['feedback']}")

with insight_col2:
    st.markdown("**Top 3 Most Negative**")
    top_neg = df.sort_values("polarity", ascending=True).head(3)
    for _, row in top_neg.iterrows():
        st.error(f"⚠️ {row['polarity']:.2f} — {row['feedback']}")

st.markdown("---")

# ----------------------------------------------------------------------------
# RAW DATA TABLE
# ----------------------------------------------------------------------------
st.subheader("📋 Full Feedback Data (with Sentiment Scores)")
display_cols = [c for c in df.columns if c != "feedback"] 
ordered_cols = [c for c in ["date", "customer_name", "product", "rating", "feedback",
                             "polarity", "subjectivity", "sentiment"] if c in df.columns]
remaining = [c for c in df.columns if c not in ordered_cols]
st.dataframe(df[ordered_cols + remaining], use_container_width=True, height=350)

csv_export = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download analyzed data as CSV",
    data=csv_export,
    file_name="analyzed_feedback.csv",
    mime="text/csv",
)

# ----------------------------------------------------------------------------
# TRY IT YOURSELF — Live sentiment checker
# ----------------------------------------------------------------------------
st.markdown("---")
st.subheader("✍️ Try It Yourself — Live Sentiment Checker")
user_text = st.text_area("Type or paste any feedback text to analyze instantly:")
if user_text.strip():
    pol, subj, label = get_sentiment(user_text)
    c1, c2, c3 = st.columns(3)
    c1.metric("Polarity", f"{pol:.3f}")
    c2.metric("Subjectivity", f"{subj:.3f}")
    c3.metric("Sentiment", label)
