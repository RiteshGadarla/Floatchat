import streamlit as st
from agents.Query import SQLagent
from agents.SummaringAgent import summarizeTable
from agents.Plotting import plotGraphs
from agents.MapAgent import generateMap
import os
import pandas as pd
import json
import uuid
import base64

# Load languages from JSON
try:
    with open("languages.json", "r") as f:
        languages_data = json.load(f)
        languages = languages_data["languages"]
        translations = languages_data["translations"]
except FileNotFoundError:
    st.error("languages.json not found. Please ensure the file exists.")
    languages = {"English": "en"}
    translations = {"en": {"title": "FloatChat - Ocean Data Exploration",
                           "markdown": "Query the oceanographic database using natural language and get summaries.",
                           "chat_input": "Enter your query...", "extracting": "Extracting data...",
                           "success": "Data retrieved successfully!", "sql_header": "Generated SQL Query",
                           "map_header": "Geographical Map", "data_header": "Data Preview",
                           "total_entries": "Total entries: {n}", "download": "Download CSV",
                           "summarizing": "Summarizing data...", "summary_header": "Data Summary",
                           "vis_header": "Visualizations", "no_plots": "No visualizations generated.",
                           "csv_not_found": "Data file not found.", "query_failed": "Query failed to execute.",
                           "voice_button_info": "Voice input not implemented yet."}}

# Page config
st.set_page_config(page_title="FloatChat", page_icon="🌊")

# Custom CSS for Ocean Theme with Fixed Layout
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(to bottom, #001f3f, #0074D9);
        color: #FFFFFF;
    }

    /* Hide default header and footer */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    footer {
        visibility: hidden;
    }

    /* Sidebar styling - Enhanced */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #001f3f 0%, #003d7a 50%, #0074D9 100%);
        color: #FFFFFF;
        padding: 0;
        border-right: 3px solid rgba(57, 204, 204, 0.3);
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
    }

    section[data-testid="stSidebar"] > div {
        padding: 20px 15px;
    }

    /* Sidebar selectbox styling */
    section[data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 20px;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(57, 204, 204, 0.5);
        border-radius: 10px;
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #39CCCC !important;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
    }

    /* Badge styling */
    .badge {
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(0, 116, 217, 0.8), rgba(57, 204, 204, 0.6));
        color: #FFFFFF;
        padding: 12px 18px;
        margin: 12px 0;
        border-radius: 15px;
        font-size: 15px;
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .badge:hover {
        transform: translateX(5px);
        background: linear-gradient(135deg, rgba(57, 204, 204, 0.9), rgba(0, 116, 217, 0.7));
        box-shadow: 0 6px 15px rgba(57, 204, 204, 0.4);
    }

    .badge img {
        margin-right: 12px;
        width: 28px;
        height: 28px;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
    }

    .badge-title {
        color: #39CCCC;
        font-size: 18px;
        font-weight: 700;
        margin: 25px 0 15px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Title styling */
    .main h1 {
        color: #FFFFFF;
        text-shadow: 0 2px 10px rgba(57, 204, 204, 0.5);
        margin-bottom: 10px;
        font-size: 2.5rem;
    }

    /* Subtitle text */
    .main p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* Main content container - proper spacing for fixed input */
    .main .block-container {
        padding-bottom: 120px !important;
        max-width: 100%;
    }

    /* Chat messages container - scrollable area */
    .chat-messages-container {
        min-height:0px;
        max-height: calc(100vh - 320px);
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 60px;
        margin-bottom: 20px;
    }

    /* Custom scrollbar for chat */
    .chat-messages-container::-webkit-scrollbar {
        width: 8px;
    }

    .chat-messages-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }

    .chat-messages-container::-webkit-scrollbar-thumb {
        background: rgba(57, 204, 204, 0.5);
        border-radius: 10px;
    }

    .chat-messages-container::-webkit-scrollbar-thumb:hover {
        background: rgba(57, 204, 204, 0.8);
    }

    /* Chat message styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px;
        padding: 18px 25px 18px 25px;        
        margin-bottom: 12px;
        color: #333333;
        border: 1px solid rgba(0, 116, 217, 0.2);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* User message specific styling */
    .stChatMessage[data-testid*="user"] {
        background: linear-gradient(135deg, rgba(0, 116, 217, 0.95), rgba(57, 204, 204, 0.85)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .stChatMessage[data-testid*="user"] p {
        color: #FFFFFF !important;
    }

    /* Hide the default streamlit chat input container */
    .stChatInputContainer {
        display: none !important;
    }

    /* Custom input container wrapper - FIXED AT BOTTOM */
    .custom-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0, 31, 63, 0.98) 85%, rgba(0, 31, 63, 0.95) 100%);
        padding: 18px 25px;
        border-top: 2px solid rgba(57, 204, 204, 0.4);
        z-index: 9999;
        backdrop-filter: blur(15px);
        box-shadow: 0 -4px 25px rgba(0, 0, 0, 0.5);
    }
    /* Center the logo image in the sidebar */
    .stImage {
        display: flex;
        justify-content: center;
    }
    /* Adjust for sidebar when expanded */
    [data-testid="stSidebar"][aria-expanded="true"] ~ .main .custom-input-container {
        margin-left: 21rem;
    }

    /* Adjust for sidebar when collapsed */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .custom-input-container {
        margin-left: 0;
    }

    /* Input row flexbox layout */
    .input-row-flex {
        display: flex;
        align-items: center;
        gap: 15px;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* Chat input takes most space */
    .input-flex-grow {
        flex: 1;
    }

    /* Mic button fixed width */
    .input-flex-shrink {
        flex-shrink: 0;
        width: 55px;
    }

    /* Chat input styling */
    .stChatInput {
        margin-bottom: 0 !important;
    }

    .stChatInput > div {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 30px !important;
        border: 2px solid #0074D9 !important;
        box-shadow: 0 4px 15px rgba(0, 116, 217, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 0 !important;
    }

    .stChatInput > div:focus-within {
        border-color: #39CCCC !important;
        box-shadow: 0 4px 20px rgba(57, 204, 204, 0.5);
        transform: translateY(-2px);
    }

    .stChatInput input {
        color: #333333 !important;
        font-size: 16px !important;
        padding: 14px 22px !important;
    }

    .stChatInput input::placeholder {
        color: rgba(51, 51, 51, 0.5) !important;
    }
.mic-button-wrapper{
    width: 75px !important;
}
    /* Mic button styling */
    .mic-button-wrapper button {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
        border-radius: 50% !important;
        border: none !important;
        width: 75px !important;
        height: 55px !important;
        min-width: 55px !important;
        min-height: 55px !important;
        padding: 0 !important;
        font-size: 26px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.5) !important;
    }

    .mic-button-wrapper button:hover {
        background: linear-gradient(135deg, #FF8E53, #FF6B6B) !important;
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.7) !important;
    }

    .mic-button-wrapper button:active {
        transform: scale(0.95) !important;
    }

    /* General button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0074D9, #39CCCC);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 116, 217, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #39CCCC, #0074D9);
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(57, 204, 204, 0.4);
    }

    /* Download button specific */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2ECC71, #27AE60) !important;
        border-radius: 20px;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #27AE60, #2ECC71) !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    /* Code block styling */
    .stCodeBlock {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 10px;
        border: 1px solid rgba(57, 204, 204, 0.3);
    }

    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #39CCCC !important;
    }

    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }

    /* Wave animation */
    @keyframes wave {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    .wave {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 100px;
        background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg"><path d="M0 60 Q 150 0 300 60 Q 450 120 600 60 Q 750 0 900 60 Q 1050 120 1200 60 L 1200 120 L 0 120 Z" fill="%23001f3f" fill-opacity="0.3"/></svg>') repeat-x;
        animation: wave 30s linear infinite;
        z-index: 10000;
        pointer-events: none;
    }

    /* Subheader styling */
    .main h2, .main h3 {
        color: #39CCCC !important;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        margin-top: 20px;
    }

    /* Prevent layout shift */
    .element-container {
        margin-bottom: 0 !important;
    }
</style>
<div class="wave"></div>
""", unsafe_allow_html=True)

# Dynamic image paths
project_root = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(project_root, "image2.png")
mic_path = os.path.join(project_root, "mic.png")
argo_path = os.path.join(project_root, "argo2.png")
ocean_path = os.path.join(project_root, "ocean.png")

# Load base64 for local images
argo_base64 = ""
ocean_base64 = ""
try:
    with open(argo_path, "rb") as f:
        argo_base64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    st.sidebar.warning("argo2.png not found")

try:
    with open(ocean_path, "rb") as f:
        ocean_base64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    st.sidebar.warning("ocean.png not found")

# Sidebar with improved UI
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.warning("Logo image not found")

    selected_lang = st.selectbox("🌐 Language", list(languages.keys()), key="lang_select")
    lang_code = languages[selected_lang]
    trans = translations.get(lang_code, translations["en"])

    st.markdown('<div class="badge-title">📊 Statistics</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div>
        <div class="badge">
            <img src="data:image/png;base64,{argo_base64}" alt="ship"/>
            <span>4,000 Argo Floats</span>
        </div>
        <div class="badge">
            <img src="https://img.icons8.com/fluency/48/calendar.png" alt="calendar"/>
            <span>2002-Present Data Archive</span>
        </div>
        <div class="badge">
            <img src="data:image/png;base64,{ocean_base64}" alt="globe"/>
            <span>All Oceans Covered</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.title(trans["title"])
st.markdown(trans["markdown"])

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Messages Container with proper scrolling
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-messages-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Display additional content like maps, dataframes, etc., if present
            if msg["role"] == "assistant" and "map_html" in msg:
                st.subheader(trans["sql_header"])
                st.code(msg.get("sql_query", ""), language="sql")
                st.subheader(trans["map_header"])
                st.components.v1.html(msg["map_html"], height=500, scrolling=True)
                if "df" in msg:
                    st.subheader(trans["data_header"])
                    st.dataframe(msg["df"], use_container_width=True)
                    st.markdown(trans["total_entries"].format(n=msg["n"]))
                    st.download_button(
                        label=trans["download"],
                        data=msg["csv_data"],
                        file_name="dataExtracted.csv",
                        mime="text/csv"
                    )
                if "summary" in msg and msg["summary"]:
                    st.subheader(trans["summary_header"])
                    st.write(msg["summary"])
                if "figures" in msg and msg["figures"]:
                    st.subheader(trans["vis_header"])
                    for fig in msg["figures"]:
                        st.pyplot(fig)
                elif "figures" in msg:
                    st.warning(trans["no_plots"])
    st.markdown('</div>', unsafe_allow_html=True)

# Custom Fixed Input Container at Bottom - Single Div
st.markdown('<div class="custom-input-container"><div class="input-row-flex">', unsafe_allow_html=True)

# Input and Mic Button in columns
col_input, col_mic = st.columns([20, 1])

with col_input:
    st.markdown('<div class="input-flex-grow">', unsafe_allow_html=True)
    user_input = st.chat_input(trans["chat_input"], key="chat_input_main")
    st.markdown('</div>', unsafe_allow_html=True)

with col_mic:
    st.markdown('<div class="input-flex-shrink"><div class="mic-button-wrapper">', unsafe_allow_html=True)
    mic_clicked = st.button("🎤", key="mic_btn", help="Voice input (coming soon)")
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Handle mic button click
if mic_clicked:
    st.session_state.messages.append({"role": "assistant", "content": trans["voice_button_info"]})
    st.rerun()

# Process User Input
if user_input:
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner(trans["extracting"]):
                sql_query = SQLagent(user_input)

                if sql_query and sql_query.get("result"):
                    st.success(trans["success"])
                    sql_string = sql_query["sql_query"]

                    map_html = generateMap(sql_string)

                    csv_path = os.path.join(project_root, "dataExtracted.csv")

                    if os.path.exists(csv_path):
                        df = pd.read_csv(csv_path)
                        n = len(df)
                        if n > 10:
                            top = df.head(5)
                            bottom = df.tail(5)
                            sep = pd.DataFrame([["..." for _ in df.columns]], columns=df.columns)
                            combined_df = pd.concat([top, sep, bottom], ignore_index=True)
                        elif n > 5:
                            top = df.head(5)
                            bottom = df.tail(n - 5)
                            sep = pd.DataFrame([["..." for _ in df.columns]], columns=df.columns)
                            combined_df = pd.concat([top, sep, bottom], ignore_index=True)
                        else:
                            combined_df = df

                        with open(csv_path, "rb") as f:
                            csv_data = f.read()

                        with st.spinner(trans["summarizing"]):
                            summary, visualizations = summarizeTable(user_input, csv_path)
                            figures = plotGraphs(csv_path, visualizations)

                        # Append assistant message with all content
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": trans.get("assistant_content", "Data processed successfully"),
                            "sql_query": sql_string,
                            "map_html": map_html,
                            "df": combined_df,
                            "n": n,
                            "csv_data": csv_data,
                            "summary": summary,
                            "figures": figures
                        })
                    else:
                        st.error(trans["csv_not_found"])
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": trans["csv_not_found"]
                        })
                else:
                    st.error(trans["query_failed"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": trans["query_failed"]
                    })

    st.rerun()