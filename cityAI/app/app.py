import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path
import time

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
# 🎨 Government-themed CSS Styling
# ============================
st.markdown("""
<style>

:root {
    --primary: #5e2d8c;     /* Deep Purple */
    --secondary: #9b59b6;   /* Medium Purple */
    --accent: #3498db;      /* Bright Blue */
    --success: #2ecc71;     /* Emerald Green */
    --warning: #f1c40f;     /* Golden Yellow */
    --danger: #e74c3c;      /* Red */
    --dark: #2c2c54;        /* Dark Navy */
    --light: #ecf0f1;       /* Light Gray */
    --card-bg: rgba(255, 255, 255, 0.95);
}

* {
    transition: all 0.2s ease;
}

body, .main {
    background: linear-gradient(135deg, #f8f9f9, #e5e8e8);
    font-family: 'Roboto', 'Segoe UI', sans-serif;
    color: var(--dark);
}

.stApp {
    background: transparent;
}

/* Government-style Header */
h1 {
    font-family: 'Roboto', sans-serif;
    font-size: 2.8rem !important;
    font-weight: 700;
    text-align: center;
    margin: 1rem 0 1.5rem;
    color: var(--primary);
    position: relative;
}

h1::after {
    content: '';
    display: block;
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    margin: 0.5rem auto 0;
    border-radius: 2px;
}

/* Professional Sidebar */
[data-testid="stSidebar"] {
    background: white !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-right: 1px solid rgba(0, 0, 0, 0.1);
}

/* Navigation Buttons */
.stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.stRadio > div > label {
    background: white !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    border-radius: 8px !important;
    padding: 0.8rem 1.2rem !important;
    color: var(--dark) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.stRadio > div > label:hover {
    background: #f2f4f4 !important;
    border-color: var(--primary) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(26, 82, 118, 0.1) !important;
}

/* Government Input Field */
.stTextInput > div > div > input {
    background: white !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    color: var(--dark) !important;
    border-radius: 8px !important;
    padding: 0.8rem !important;
    font-size: 1rem !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(26, 82, 118, 0.2) !important;
    outline: none !important;
}

/* Government Cards */
.card {
    background: var(--card-bg) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    margin-bottom: 1.2rem !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05) !important;
    position: relative !important;
    overflow: hidden !important;
}

.card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
}

/* Government Button */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 8px rgba(26, 82, 118, 0.2) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(26, 82, 118, 0.3) !important;
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    background: rgba(26, 82, 118, 0.1);
    color: var(--primary);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--primary);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-positive {
    background: rgba(39, 174, 96, 0.1);
    color: var(--success);
}

.badge-negative {
    background: rgba(231, 76, 60, 0.1);
    color: var(--danger);
}

.badge-neutral {
    background: rgba(243, 156, 18, 0.1);
    color: var(--warning);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.4s ease-out;
}

/* Alert Boxes */
.stAlert {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================
# 🎮 Sidebar Navigation
# ============================
with st.sidebar:
    st.markdown("""
    <style>
        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important;
            color: white !important;
            padding-top: 1.5rem;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            box-shadow: 5px 0 15px rgba(0, 0, 0, 0.3);
        }

        /* Sidebar Header */
        .sidebar-header h2 {
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
            color: #ffffff;
            font-weight: 700;
            letter-spacing: 1px;
        }

        /* Divider Line */
        .sidebar-divider {
            height: 2px;
            width: 60px;
            margin: 0.5rem auto 1rem;
            background: linear-gradient(90deg, #ffffffcc, #ffffff44);
            border-radius: 2px;
        }

        /* Navigation Radio Buttons */
        .sidebar-nav label {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 0.6rem 1rem !important;
            margin-bottom: 0.5rem !important;
            transition: all 0.3s ease !important;
            color: #f0f0f0 !important;
            font-size: 1rem !important;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-nav label:hover {
            background-color: rgba(255, 255, 255, 0.15) !important;
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .sidebar-nav input[type="radio"] {
            display: none;
        }

        .sidebar-nav label[aria-checked="true"] {
            background-color: rgba(255, 255, 255, 0.25) !important;
            font-weight: bold;
            color: #fffde7 !important;
            box-shadow: inset 0 0 0 2px #ffffff66;
            border-color: rgba(255, 255, 255, 0.3);
        }
    </style>

    <div class="sidebar-header" style="text-align: center; margin-bottom: 1.5rem;">
        <h2>Citizen AI</h2>
        <div class="sidebar-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    menu = ["AI Assistant", "Sentiment Analysis", "Citizen Dashboard", "System Settings"]
    icons = ["💬", "📊", "📈", "⚙️"]

    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    choice = st.radio(
        "NAVIGATION",
        menu,
        format_func=lambda x: f"{icons[menu.index(x)]} {x}",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
# ============================
# 🛰️ API & Data Paths
# ============================
ROOT_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_FILE = ROOT_DIR / "data" / "feedback.json"
API_CHAT_URL = "https://cityai-wfn8.onrender.com/chat"

# ============================
# 💬 AI Assistant Interface
# ============================
if choice == "AI Assistant":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1>Citizen AI Assistant</h1>
        <p style="color: #5d6d7e; max-width: 700px; margin: 0 auto;">Ask questions about government services, policies, or civic issues and receive instant, accurate responses.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: var(--primary);">Government Services Assistant</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Active</span>
            </div>
        </div>
        <p style="color: #5d6d7e; margin-bottom: 0;">Powered by IBM Granite models for accurate, contextual responses to your civic inquiries.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        query = st.text_input(
            "Your civic inquiry...",
            placeholder="Ask about taxes, services, policies, or report issues...",
            key="chat_input"
        )

        col1 = st.columns([1, 5])[0]  # Only get first column
        with col1:
            submit_clicked = st.button("Submit Inquiry", key="chat_submit")

    # New container for output to isolate layout
    output_container = st.container()

    if submit_clicked:
        if not query.strip():
            output_container.warning("Please enter a question before submitting.")
        else:
            with output_container:
                with st.spinner("Processing your civic inquiry..."):
                    try:
                        response = requests.post(API_CHAT_URL, json={"query": query})
                        response.raise_for_status()
                        result = response.json()

                        st.markdown(f"""
                        <div class="card fade-in">
                            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div style="width: 8px; height: 8px; background: var(--primary); border-radius: 50%;"></div>
                                <h4 style="margin: 0; color: var(--primary);">Government Response</h4>
                            </div>
                            <div style="margin-top: 0.5rem; padding-left: 1rem; color: #2c3e50;">
                                {result.get('reply', 'We could not process your inquiry at this time. Please try again later.')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        sentiment = result.get('sentiment', 'NEUTRAL')
                        sentiment_class = f"badge-{sentiment.lower()}"

                        st.markdown(f"""
                        <div class="card fade-in" style="animation-delay: 0.2s;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <div style="width: 8px; height: 8px; background: var(--primary); border-radius: 50%;"></div>
                                    <h4 style="margin: 0; color: var(--primary);">Sentiment Detected</h4>
                                </div>
                                <span class="badge {sentiment_class}">{sentiment}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    except requests.exceptions.RequestException as e:
                        st.error(f"Service unavailable: Please ensure the backend service is running. Error: {str(e)}")
                    except json.JSONDecodeError:
                        st.error("Invalid response format from government service")
                    except Exception as e:
                        st.error(f"Error processing your inquiry: {str(e)}")
# ============================
# 📊 Sentiment Analysis Dashboard
# ============================
elif choice == "Sentiment Analysis":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1>Citizen Sentiment Analysis</h1>
        <p style="color: #5d6d7e; max-width: 700px; margin: 0 auto;">Understand public sentiment about government services and policies.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: var(--primary);">Public Sentiment Monitor</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Live Analysis</span>
            </div>
        </div>
        <p style="color: #5d6d7e; margin-bottom: 0;">Powered by IBM Watson to analyze citizen feedback and identify areas needing attention.</p>
    </div>
    """, unsafe_allow_html=True)

    if FEEDBACK_FILE.exists() and FEEDBACK_FILE.stat().st_size > 0:
        try:
            with open(FEEDBACK_FILE, "r") as f:
                data = json.load(f)

            if not data:
                st.warning("No citizen feedback data available yet.")
            else:
                df = pd.DataFrame(data)

                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                else:
                    df['timestamp'] = pd.to_datetime([datetime.now()] * len(df))

                df['sentiment'] = df['sentiment'].astype(str)

                # Create columns for the dashboard
                col1,col2 = st.columns(2)

                with col1:
                    st.markdown("""
                    <div style="margin-bottom: 1rem;">
                        <h3>Sentiment Distribution</h3>
                        <div style="height: 2px; background: linear-gradient(90deg, var(--primary), var(--secondary)); margin-bottom: 0.5rem; width: 60px; border-radius: 2px;"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    pie_fig = px.pie(
                        df,
                        names='sentiment',
                        title='',
                        hole=0.4,
                        color_discrete_map={
                            "POSITIVE": "#27ae60",
                            "NEGATIVE": "#e74c3c",
                            "NEUTRAL": "#f39c12"
                        }
                    )

                    pie_fig.update_layout(
                        margin=dict(l=20, r=20, t=30, b=20),
                        font=dict(size=14, color="#2c3e50"),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.2,
                            xanchor="center",
                            x=0.5
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )

                    st.plotly_chart(pie_fig, use_container_width=True)

                with col2:
                    st.markdown("""
                    <div style="margin-bottom: 1rem;">
                        <h3>Weekly Trend</h3>
                        <div style="height: 2px; background: linear-gradient(90deg, var(--primary), var(--secondary)); margin-bottom: 0.5rem; width: 60px; border-radius: 2px;"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    trend_data = df.groupby([df['timestamp'].dt.date, 'sentiment']).size().reset_index(name='count')
                    trend_data.rename(columns={'timestamp': 'date'}, inplace=True)

                    line_fig = px.line(
                        trend_data,
                        x='date',
                        y='count',
                        color='sentiment',
                        line_shape="spline",
                        markers=True,
                        color_discrete_map={
                            "POSITIVE": "#27ae60",
                            "NEGATIVE": "#e74c3c",
                            "NEUTRAL": "#f39c12"
                        }
                    )

                    line_fig.update_layout(
                        margin=dict(l=20, r=20, t=30, b=20),
                        font=dict(size=14, color="#2c3e50"),
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

                # Recent Feedback Table
                st.markdown("""
                <div style="margin: 1.5rem 0 0.5rem;">
                    <h3>Recent Citizen Feedback</h3>
                    <div style="height: 2px; background: linear-gradient(90deg, var(--primary), var(--secondary)); margin-bottom: 0.5rem; width: 60px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)

                st.dataframe(
                    df[['timestamp', 'user_query', 'reply', 'sentiment']].tail(10).iloc[::-1],
                    use_container_width=True,
                    column_config={
                        "timestamp": "Date/Time",
                        "user_query": "Citizen Inquiry",
                        "reply": "Government Response",
                        "sentiment": "Sentiment"
                    }
                )

        except json.JSONDecodeError:
            st.error("Invalid data format in feedback records")
        except Exception as e:
            st.error(f"Error loading citizen feedback: {str(e)}")
    else:
        st.warning("No citizen feedback data available yet.")

# ============================
# 📈 Citizen Dashboard Interface
# ============================
elif choice == "Citizen Dashboard":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1>Citizen Engagement Dashboard</h1>
        <p style="color: #5d6d7e; max-width: 700px; margin: 0 auto;">Real-time insights into citizen-government interactions and service performance.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: var(--primary);">Government Analytics</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Secure Connection</span>
            </div>
        </div>
        <p style="color: #5d6d7e; margin-bottom: 0;">Comprehensive metrics to enhance public service delivery and citizen satisfaction.</p>
    </div>
    """, unsafe_allow_html=True)

    if FEEDBACK_FILE.exists() and FEEDBACK_FILE.stat().st_size > 0:
        try:
            with open(FEEDBACK_FILE, "r") as f:
                data = json.load(f)

            if not data:
                st.warning("No interaction data available yet.")
            else:
                df = pd.DataFrame(data)

                if 'timestamp' not in df.columns:
                    df['timestamp'] = pd.to_datetime([datetime.now()] * len(df))
                else:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])

                # KPI Cards
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("""
                    <div class="card" style="text-align: center;">
                        <h4 style="color: var(--primary); margin-bottom: 0.5rem;">Total Interactions</h4>
                        <h2 style="color: var(--secondary); margin-top: 0;">{}</h2>
                    </div>
                    """.format(len(df)), unsafe_allow_html=True)

                with col2:
                    positive_pct = len(df[df['sentiment'] == 'POSITIVE']) / len(df) * 100
                    st.markdown("""
                    <div class="card" style="text-align: center;">
                        <h4 style="color: var(--primary); margin-bottom: 0.5rem;">Positive Sentiment</h4>
                        <h2 style="color: var(--success); margin-top: 0;">{:.1f}%</h2>
                    </div>
                    """.format(positive_pct), unsafe_allow_html=True)

                with col3:
                    avg_response_time = "N/A"  # Placeholder for actual metric
                    st.markdown("""
                    <div class="card" style="text-align: center;">
                        <h4 style="color: var(--primary); margin-bottom: 0.5rem;">Avg. Response Time</h4>
                        <h2 style="color: var(--secondary); margin-top: 0;">{}</h2>
                    </div>
                    """.format(avg_response_time), unsafe_allow_html=True)

                # Service Category Analysis
                st.markdown("""
                <div style="margin: 1.5rem 0 0.5rem;">
                    <h3>Service Category Analysis</h3>
                    <div style="height: 2px; background: linear-gradient(90deg, var(--primary), var(--secondary)); margin-bottom: 0.5rem; width: 60px; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)

                # Placeholder for service category analysis
                st.warning("Service categorization feature coming soon")

        except Exception as e:
            st.error(f"Error loading dashboard data: {str(e)}")
    else:
        st.warning("No interaction data available yet.")

# ============================
# ⚙️ System Settings Interface
# ============================
elif choice == "System Settings":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1>System Configuration</h1>
        <p style="color: #5d6d7e; max-width: 700px; margin: 0 auto;">Administrative settings for the Citizen AI platform.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: var(--primary);">Platform Settings</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Admin Mode</span>
            </div>
        </div>
        <p style="color: #5d6d7e; margin-bottom: 0;">Configure system parameters and integration settings.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("system_config"):
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                "Response Style",
                ["Formal", "Balanced", "Friendly"],
                index=0,
                help="Tone of government responses"
            )

            st.slider(
                "Response Detail Level",
                min_value=1,
                max_value=5,
                value=3,
                help="Amount of detail in responses"
            )

        with col2:
            st.selectbox(
                "AI Model",
                ["IBM Granite Standard", "IBM Granite Advanced", "IBM Watson"],
                index=0,
                help="Underlying AI model for responses"
            )

            st.toggle(
                "Enable Follow-up Suggestions",
                value=True,
                help="Show suggested follow-up questions"
            )

        if st.form_submit_button("Save Configuration"):
            st.success("System configuration updated successfully")
            time.sleep(1)
