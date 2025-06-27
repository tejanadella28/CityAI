import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path
import time
import os
import io
import logging

# ============================
# 🔍 Setup Logging for Debugging
# ============================
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================
# 🔮 Page Configuration
# ============================
st.set_page_config(
    page_title="Citizen AI - Government Engagement Platform",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏛️"
)

# ============================
# 🎨 Sleek Government-themed CSS Styling
# ============================
st.markdown("""
<style>
:root {
    --primary: #1e40af;     /* Deep Blue */
    --secondary: #3b82f6;   /* Bright Blue */
    --accent: #d97706;      /* Warm Gold */
    --success: #22c55e;     /* Green */
    --warning: #eab308;     /* Yellow */
    --danger: #ef4444;      /* Red */
    --dark: #111827;        /* Dark Gray */
    --light: #f9fafb;       /* Light Gray */
    --card-bg: rgba(255, 255, 255, 0.99);
}

* {
    transition: all 0.3s ease;
    box-sizing: border-box;
}

body, .main {
    background: linear-gradient(145deg, #f3f4f6, #e5e7eb);
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #111827; /* Hardcoded --dark */
}

.stApp {
    background: transparent;
}

/* Modern Header */
h1 {
    font-family: 'Inter', sans-serif;
    font-size: 2.6rem !important;
    font-weight: 600;
    text-align: center;
    margin: 2rem 0 1.3rem;
    color: #1e40af; /* Hardcoded --primary */
    letter-spacing: -0.3px;
}

h1::after {
    content: '';
    display: block;
    width: 110px;
    height: 4px;
    background: linear-gradient(90deg, #1e40af, #d97706); /* Hardcoded --primary, --accent */
    margin: 0.9rem auto 0;
    border-radius: 2px;
}

/* Professional Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e40af, #1e3a8a) !important; /* Hardcoded --primary, darker shade */
    color: white !important;
    padding: 2rem 1.5rem;
    border-right: none;
    box-shadow: 3px 0 15px rgba(0, 0, 0, 0.25);
}

/* Navigation Buttons */
.stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
}

.stRadio > div > label {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.7rem !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 1.05rem !important;
    cursor: pointer;
}

.stRadio > div > label:hover {
    background: rgba(255, 255, 255, 0.2) !important;
    border-color: #d97706 !important; /* Hardcoded --accent */
    transform: translateX(6px);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}

.stRadio > div > label[data-checked="true"] {
    background: #d97706 !important; /* Hardcoded --accent */
    border-color: #d97706 !important;
    color: #111827 !important; /* Hardcoded --dark */
    font-weight: 600 !important;
}

/* Input Fields */
.stTextInput > div > div > input {
    background: white !important;
    border: 1px solid #d1d5db !important;
    border-radius: 14px !important;
    padding: 1.1rem !important;
    font-size: 1.05rem !important;
    color: #111827 !important; /* Hardcoded --dark */
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #d97706 !important; /* Hardcoded --accent */
    box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.2) !important;
    outline: none !important;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.99) !important; /* Hardcoded --card-bg */
    border-radius: 18px !important;
    padding: 2.2rem !important;
    margin-bottom: 2.2rem !important;
    border: 1px solid rgba(0, 0, 0, 0.05) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12) !important;
}

.card:hover {
    transform: translateY(-6px) !important;
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.18) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1e40af, #d97706) !important; /* Hardcoded --primary, --accent */
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 1rem 2.2rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
    background: linear-gradient(135deg, #d97706, #1e40af) !important; /* Hardcoded --accent, --primary */
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.7rem 1.3rem;
    border-radius: 28px;
    font-size: 0.95rem;
    font-weight: 500;
    background: rgba(217, 119, 6, 0.1); /* Hardcoded --accent with opacity */
    color: #d97706; /* Hardcoded --accent */
}

.status-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #d97706; /* Hardcoded --accent */
    animation: pulse 1.4s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.5rem 1.1rem;
    border-radius: 18px;
    font-size: 0.95rem;
    font-weight: 600;
}

.badge-positive {
    background: rgba(34, 197, 94, 0.1);
    color: #22c55e; /* Hardcoded --success */
}

.badge-negative {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444; /* Hardcoded --danger */
}

.badge-neutral {
    background: rgba(234, 179, 8, 0.1);
    color: #eab308; /* Hardcoded --warning */
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.8s ease-out;
}

/* Alert Boxes */
.stAlert {
    border-radius: 14px !important;
    padding: 1.3rem !important;
    font-size: 0.95rem !important;
}

/* Form Styling */
.stForm {
    background: white !important;
    padding: 2.2rem !important;
    border-radius: 18px !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12) !important;
}

.stSelectbox, .stSlider, .stToggle {
    background: white !important;
    border-radius: 14px !important;
    padding: 0.7rem !important;
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #3b82f6, #d97706) !important; /* Hardcoded --secondary, --accent */
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 1rem 2.2rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
    background: linear-gradient(135deg, #d97706, #3b82f6) !important; /* Hardcoded --accent, --secondary */
}
</style>
""", unsafe_allow_html=True)

# ============================
# 🎮 Sidebar Navigation
# ============================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2 style="font-family: 'Inter', sans-serif; font-size: 2rem; margin-bottom: 0.3rem; color: white; font-weight: 600; letter-spacing: 0.2px; text-align: center;">
            Citizen AI
        </h2>
        <div style="height: 4px; width: 80px; margin: 0.9rem auto 1.5rem; background: linear-gradient(90deg, #d97706, #3b82f6); border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    menu = ["AI Assistant", "Sentiment Analysis", "Citizen Dashboard", "System Settings"]
    icons = ["💬", "📊", "📈", "⚙️"]

    choice = st.radio(
        "NAVIGATION",
        menu,
        format_func=lambda x: f"{icons[menu.index(x)]} {x}",
        label_visibility="collapsed"
    )

# ============================
# 🛰️ API & Data Paths
# ============================
ROOT_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_FILE = ROOT_DIR / "data" / "feedback.json"
API_CHAT_URL = "http://127.0.0.1:5000/chat"

# Ensure feedback.json exists and is writable
try:
    if not FEEDBACK_FILE.parent.exists():
        FEEDBACK_FILE.parent.mkdir(parents=True)
        logger.debug(f"Created directory: {FEEDBACK_FILE.parent}")
    if not FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([], f)
        logger.debug(f"Created empty feedback.json at {FEEDBACK_FILE}")
    if not os.access(FEEDBACK_FILE, os.R_OK | os.W_OK):
        logger.error(f"Feedback file {FEEDBACK_FILE} is not readable/writable")
        st.error(f"Permission denied for {FEEDBACK_FILE}. Please check file permissions.")
except Exception as e:
    logger.error(f"Error initializing feedback.json: {str(e)}")
    st.error(f"Failed to initialize feedback.json: {str(e)}")

# ============================
# 💬 AI Assistant Interface
# ============================
if choice == "AI Assistant":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <h1>Citizen AI Assistant</h1>
        <p style="color: #6b7280; max-width: 700px; margin: 0 auto; font-size: 1rem;">Engage with government services, ask about policies, or report civic issues with instant, accurate responses.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.5rem; color: #1e40af;">Government Services Assistant</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Online</span>
            </div>
        </div>
        <p style="color: #6b7280; margin-bottom: 0; font-size: 0.95rem;">Powered by advanced AI models for reliable and contextual civic assistance.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input(
                "Your civic inquiry...",
                placeholder="Ask about taxes, services, policies, or report issues...",
                key="chat_input"
            )
        with col2:
            submit_clicked = st.button("Submit", key="chat_submit")

    output_container = st.container()
    if submit_clicked:
        if not query.strip():
            output_container.warning("Please enter a question before submitting.")
        else:
            with output_container:
                with st.spinner("Processing your inquiry..."):
                    try:
                        response = requests.post(API_CHAT_URL, json={"query": query})
                        response.raise_for_status()
                        result = response.json()
                        logger.debug(f"API response: {result}")

                        st.markdown("""
                        <div class="card fade-in">
                            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;">
                                <div style="width: 14px; height: 14px; background: #d97706; border-radius: 50%;"></div>
                                <h4 style="margin: 0; font-size: 1.3rem; color: #1e40af;">Response</h4>
                            </div>
                            <div style="margin-top: 0.5rem; padding-left: 1.5rem; font-size: 0.95rem; color: #111827;">
                                {}
                            </div>
                        </div>
                        """.format(result.get('reply', 'We could not process your inquiry at this time. Please try again later.')), unsafe_allow_html=True)

                        sentiment = result.get('sentiment', 'NEUTRAL')
                        sentiment_class = f"badge-{sentiment.lower()}"

                        st.markdown("""
                        <div class="card fade-in" style="animation-delay: 0.3s;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.8rem;">
                                    <div style="width: 14px; height: 14px; background: #d97706; border-radius: 50%;"></div>
                                    <h4 style="margin: 0; font-size: 1.3rem; color: #1e40af;">Sentiment</h4>
                                </div>
                                <span class="badge {}">{}</span>
                            </div>
                        </div>
                        """.format(sentiment_class, sentiment), unsafe_allow_html=True)

                        # Feedback Submission Feature
                        st.markdown("""
                        <div class="card fade-in" style="animation-delay: 0.5s;">
                            <h4 style="margin: 0 0 1rem; font-size: 1.3rem; color: #1e40af;">Rate this Response</h4>
                            <p style="color: #6b7280; font-size: 0.95rem;">Was this response helpful?</p>
                        </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("👍 Thumbs Up", key="thumbs_up"):
                                feedback_rating = "POSITIVE"
                                feedback_data = {
                                    "timestamp": datetime.now().isoformat(),
                                    "user_query": query,
                                    "reply": result.get('reply', ''),
                                    "sentiment": sentiment,
                                    "user_rating": feedback_rating
                                }
                                try:
                                    with open(FEEDBACK_FILE, "r+") as f:
                                        try:
                                            data = json.load(f)
                                            logger.debug(f"Loaded feedback.json for writing: {len(data)} records")
                                        except json.JSONDecodeError:
                                            logger.warning("Corrupted feedback.json detected, resetting to empty list")
                                            data = []
                                        data.append(feedback_data)
                                        f.seek(0)
                                        json.dump(data, f, indent=2)
                                        logger.debug("Feedback saved successfully")
                                    st.success("Thank you for your feedback!")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    logger.error(f"Error writing feedback: {str(e)}")
                                    st.error(f"Failed to save feedback: {str(e)}")
                        with col2:
                            if st.button("👎 Thumbs Down", key="thumbs_down"):
                                feedback_rating = "NEGATIVE"
                                feedback_data = {
                                    "timestamp": datetime.now().isoformat(),
                                    "user_query": query,
                                    "reply": result.get('reply', ''),
                                    "sentiment": sentiment,
                                    "user_rating": feedback_rating
                                }
                                try:
                                    with open(FEEDBACK_FILE, "r+") as f:
                                        try:
                                            data = json.load(f)
                                            logger.debug(f"Loaded feedback.json for writing: {len(data)} records")
                                        except json.JSONDecodeError:
                                            logger.warning("Corrupted feedback.json detected, resetting to empty list")
                                            data = []
                                        data.append(feedback_data)
                                        f.seek(0)
                                        json.dump(data, f, indent=2)
                                        logger.debug("Feedback saved successfully")
                                    st.success("Thank you for your feedback!")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    logger.error(f"Error writing feedback: {str(e)}")
                                    st.error(f"Failed to save feedback: {str(e)}")

                    except requests.exceptions.RequestException as e:
                        logger.error(f"API request failed: {str(e)}")
                        st.error(f"Service unavailable: Please ensure the backend service is running. Error: {str(e)}")
                    except json.JSONDecodeError:
                        logger.error("Invalid JSON response from API")
                        st.error("Invalid response format from government service")
                    except Exception as e:
                        logger.error(f"Unexpected error in AI Assistant: {str(e)}")
                        st.error(f"Error processing your inquiry: {str(e)}")

# ============================
# 📊 Sentiment Analysis Dashboard
# ============================
elif choice == "Sentiment Analysis":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <h1>Sentiment Analysis</h1>
        <p style="color: #6b7280; max-width: 700px; margin: 0 auto; font-size: 1rem;">Gain insights into public sentiment regarding government services and policies.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.5rem; color: #1e40af;">Public Sentiment Monitor</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Live Analysis</span>
            </div>
        </div>
        <p style="color: #6b7280; margin-bottom: 0; font-size: 0.95rem;">Real-time analysis of citizen feedback to identify trends and areas for improvement.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        if not FEEDBACK_FILE.exists() or FEEDBACK_FILE.stat().st_size == 0:
            logger.warning("Feedback file missing or empty")
            st.warning("No citizen feedback data available yet. Please ensure feedback.json exists and contains valid data.")
        else:
            with open(FEEDBACK_FILE, "r") as f:
                try:
                    data = json.load(f)
                    logger.debug(f"Loaded feedback.json with {len(data)} records")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse feedback.json: {str(e)}")
                    st.error(f"Failed to parse feedback.json: {str(e)}. Please ensure the file contains valid JSON.")
                    data = None

            if not data or not isinstance(data, list):
                logger.warning("Feedback data is empty or not a list")
                st.warning("No valid citizen feedback data available in feedback.json.")
            else:
                df = pd.DataFrame(data)
                logger.debug(f"DataFrame created with shape {df.shape}")

                # Define expected columns
                expected_columns = ['timestamp', 'user_query', 'reply', 'sentiment', 'user_rating']
                for col in expected_columns:
                    if col not in df.columns:
                        df[col] = None
                        logger.debug(f"Added missing column: {col}")

                # Handle timestamp
                if df['timestamp'].isna().all():
                    df['timestamp'] = pd.to_datetime([datetime.now()] * len(df))
                    logger.debug("Set default timestamps")
                else:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    logger.debug("Converted timestamps")

                # Ensure sentiment and user_rating are strings
                df['sentiment'] = df['sentiment'].fillna('NEUTRAL').astype(str)
                df['user_rating'] = df['user_rating'].fillna('NEUTRAL').astype(str)
                logger.debug("Normalized sentiment and user_rating columns")

                # New Search Feature
                st.markdown("""
                <div style="margin: 2.5rem 0 1rem;">
                    <h3 style="font-size: 1.4rem; color: #1e40af;">Search Feedback</h3>
                    <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)

                search_query = st.text_input(
                    "Search feedback by query or response...",
                    placeholder="Enter keywords to search...",
                    key="search_feedback"
                )

                filtered_df = df
                if search_query.strip():
                    filtered_df = df[
                        df['user_query'].str.contains(search_query, case=False, na=False) |
                        df['reply'].str.contains(search_query, case=False, na=False)
                    ]
                    logger.debug(f"Search applied, filtered DataFrame shape: {filtered_df.shape}")

                # Filtering Feature
                st.markdown("""
                <div style="margin: 2.5rem 0 1rem;">
                    <h3 style="font-size: 1.4rem; color: #1e40af;">Filter Feedback</h3>
                    <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)

                filter_option = st.selectbox(
                    "Filter by Sentiment or Rating",
                    ["All", "Positive Sentiment", "Negative Sentiment", "Neutral Sentiment", "Positive Rating", "Negative Rating", "Neutral Rating"],
                    key="filter_feedback"
                )

                if filter_option != "All":
                    if "Sentiment" in filter_option:
                        sentiment_value = filter_option.split()[0].upper()
                        filtered_df = filtered_df[filtered_df['sentiment'] == sentiment_value]
                    elif "Rating" in filter_option:
                        rating_value = filter_option.split()[0].upper()
                        filtered_df = filtered_df[filtered_df['user_rating'] == rating_value]
                    logger.debug(f"Filter applied, filtered DataFrame shape: {filtered_df.shape}")

                # Export Feature
                st.markdown("""
                <div style="margin: 2.5rem 0 1rem;">
                    <h3 style="font-size: 1.4rem; color: #1e40af;">Export Feedback Data</h3>
                    <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download Filtered Feedback as CSV",
                    data=csv,
                    file_name="citizen_feedback_filtered.csv",
                    mime="text/csv",
                    key="download_feedback"
                )

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div style="margin-bottom: 1.3rem;">
                        <h3 style="font-size: 1.4rem; color: #1e40af;">Sentiment Distribution</h3>
                        <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    pie_fig = px.pie(
                        filtered_df,
                        names='sentiment',
                        title='',
                        hole=0.5,
                        color_discrete_map={
                            "POSITIVE": "#22c55e",
                            "NEGATIVE": "#ef4444",
                            "NEUTRAL": "#eab308"
                        }
                    )

                    pie_fig.update_layout(
                        margin=dict(l=20, r=20, t=20, b=20),
                        font=dict(size=14, color='#111827'),  # Hardcoded --dark
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.3,
                            xanchor="center",
                            x=0.5
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )

                    st.plotly_chart(pie_fig, use_container_width=True)

                with col2:
                    st.markdown("""
                    <div style="margin-bottom: 1.3rem;">
                        <h3 style="font-size: 1.4rem; color: #1e40af;">Weekly Trend</h3>
                        <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    trend_data = filtered_df.groupby([filtered_df['timestamp'].dt.date, 'sentiment']).size().reset_index(name='count')
                    trend_data.rename(columns={'timestamp': 'date'}, inplace=True)

                    line_fig = px.line(
                        trend_data,
                        x='date',
                        y='count',
                        color='sentiment',
                        line_shape="spline",
                        markers=True,
                        color_discrete_map={
                            "POSITIVE": "#22c55e",
                            "NEGATIVE": "#ef4444",
                            "NEUTRAL": "#eab308"
                        }
                    )

                    line_fig.update_layout(
                        margin=dict(l=20, r=20, t=20, b=20),
                        font=dict(size=14, color='#111827'),  # Hardcoded --dark
                        xaxis_title="Date",
                        yaxis_title="Feedback Count",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.3,
                            xanchor="center",
                            x=0.5
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )

                    st.plotly_chart(line_fig, use_container_width=True)

                st.markdown("""
                <div style="margin: 2.5rem 0 1rem;">
                    <h3 style="font-size: 1.4rem; color: #1e40af;">Recent Feedback</h3>
                    <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)

                display_columns = [col for col in ['timestamp', 'user_query', 'reply', 'sentiment', 'user_rating'] if col in filtered_df.columns]
                st.dataframe(
                    filtered_df[display_columns].tail(10).iloc[::-1],
                    use_container_width=True,
                    column_config={
                        "timestamp": "Date/Time",
                        "user_query": "Citizen Inquiry",
                        "reply": "Government Response",
                        "sentiment": "Sentiment",
                        "user_rating": "User Rating"
                    }
                )

    except Exception as e:
        logger.error(f"Error in Sentiment Analysis: {str(e)}")
        st.error(f"Error loading citizen feedback: {str(e)}. Please ensure feedback.json is valid and accessible.")

# ============================
# 📈 Citizen Dashboard Interface
# ============================
elif choice == "Citizen Dashboard":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <h1>Citizen Engagement Dashboard</h1>
        <p style="color: #6b7280; max-width: 700px; margin: 0 auto; font-size: 1rem;">Real-time insights into citizen-government interactions and service performance.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.5rem; color: #1e40af;">Government Analytics</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Secure Connection</span>
            </div>
        </div>
        <p style="color: #6b7280; margin-bottom: 0; font-size: 0.95rem;">Metrics to enhance public service delivery and citizen satisfaction.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        if not FEEDBACK_FILE.exists() or FEEDBACK_FILE.stat().st_size == 0:
            logger.warning("Feedback file missing or empty in Citizen Dashboard")
            st.warning("No interaction data available yet. Please ensure feedback.json exists and contains valid data.")
        else:
            with open(FEEDBACK_FILE, "r") as f:
                try:
                    data = json.load(f)
                    logger.debug(f"Loaded feedback.json with {len(data)} records for dashboard")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse feedback.json in dashboard: {str(e)}")
                    st.error(f"Failed to parse feedback.json: {str(e)}. Please ensure the file contains valid JSON.")
                    data = None

            if not data or not isinstance(data, list):
                logger.warning("Dashboard feedback data is empty or not a list")
                st.warning("No valid interaction data available in feedback.json.")
            else:
                df = pd.DataFrame(data)

                # Define expected columns
                expected_columns = ['timestamp', 'user_query', 'reply', 'sentiment', 'user_rating']
                for col in expected_columns:
                    if col not in df.columns:
                        df[col] = None
                        logger.debug(f"Added missing column in dashboard: {col}")

                if 'timestamp' not in df.columns or df['timestamp'].isna().all():
                    df['timestamp'] = pd.to_datetime([datetime.now()] * len(df))
                    logger.debug("Set default timestamps in dashboard")
                else:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    logger.debug("Converted timestamps in dashboard")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    <div class="card" style="text-align: center;">
                        <h4 style="color: #1e40af; margin-bottom: 0.8rem; font-size: 1.25rem;">Total Interactions</h4>
                        <h2 style="color: #d97706; margin-top: 0; font-size: 2.3rem;">{}</h2>
                    </div>
                    """.format(len(df)), unsafe_allow_html=True)

                with col2:
                    positive_pct = len(df[df['sentiment'] == 'POSITIVE']) / len(df) * 100 if 'sentiment' in df.columns else 0
                    st.markdown("""
                    <div class="card" style="text-align: center;">
                        <h4 style="color: #1e40af; margin-bottom: 0.8rem; font-size: 1.25rem;">Positive Sentiment</h4>
                        <h2 style="color: #22c55e; margin-top: 0; font-size: 2.3rem;">{:.1f}%</h2>
                    </div>
                    """.format(positive_pct), unsafe_allow_html=True)

                with col3:
                    avg_response_time = "N/A"
                    st.markdown("""
                    <div class="card" style="text-align: center;">
                        <h4 style="color: #1e40af; margin-bottom: 0.8rem; font-size: 1.25rem;">Avg. Response Time</h4>
                        <h2 style="color: #d97706; margin-top: 0; font-size: 2.3rem;">{}</h2>
                    </div>
                    """.format(avg_response_time), unsafe_allow_html=True)

                st.markdown("""
                <div style="margin: 2.5rem 0 1rem;">
                    <h3 style="font-size: 1.4rem; color: #1e40af;">Service Category Analysis</h3>
                    <div style="height: 4px; background: linear-gradient(90deg, #1e40af, #d97706); margin-bottom: 1rem; width: 80px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)

                st.warning("Service categorization feature coming soon")

    except Exception as e:
        logger.error(f"Error in Citizen Dashboard: {str(e)}")
        st.error(f"Error loading dashboard data: {str(e)}. Please ensure feedback.json is valid and accessible.")

# ============================
# ⚙️ System Settings Interface
# ============================
elif choice == "System Settings":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <h1>System Configuration</h1>
        <p style="color: #6b7280; max-width: 700px; margin: 0 auto; font-size: 1rem;">Customize the Citizen AI platform to meet administrative needs.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.5rem; color: #1e40af;">Platform Settings</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Admin Mode</span>
            </div>
        </div>
        <p style="color: #6b7280; margin-bottom: 0; font-size: 0.95rem;">Adjust system parameters and integration settings.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("system_config"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                "Response Style",
                ["Formal", "Balanced", "Friendly"],
                index=0,
                help="Set the tone for government responses"
            )
            st.slider(
                "Response Detail Level",
                min_value=1,
                max_value=5,
                value=3,
                help="Control the level of detail in responses"
            )
        with col2:
            st.selectbox(
                "AI Model",
                ["IBM Granite Standard", "IBM Granite Advanced", "IBM Watson"],
                index=0,
                help="Select the AI model for responses"
            )
            st.toggle(
                "Enable Follow-up Suggestions",
                value=True,
                help="Show suggested follow-up questions"
            )
        if st.form_submit_button("Save Configuration"):
            st.success("Configuration updated successfully")
            time.sleep(1)