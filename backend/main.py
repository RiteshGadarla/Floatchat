import streamlit as st
from agents.Query import SQLagent
from agents.SummaringAgent import summarizeTable
from agents.Plotting import plotGraphs
import os
import pandas as pd

# # === Streamlit Config ===
# st.set_page_config(page_title="🌊 FloatChat - Ocean Data Agent", layout="wide")
#
# st.title("🌊 FloatChat - Ocean Data Exploration")
# st.markdown("Query the oceanographic database using natural language and get summaries.")

# === Chat History (session state) ===
if "messages" not in st.session_state:
    st.session_state.messages = []  # stores user + assistant with results

# Show chat history (including results)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg.get("summary"):
            st.subheader("📌 Summary")
            st.write(msg["summary"])

        if msg.get("figures"):
            for fig in msg["figures"]:
                st.pyplot(fig)

# === User Input at Bottom  ===
if user_input := st.chat_input("🔍 Enter your query..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Run query
    with st.chat_message("assistant"):
        with st.spinner("⏳ Generating SQL and extracting data..."):
            result = SQLagent(user_input)

        if result and result.get("result"):
            st.success("✅ Query executed successfully!")

            # Placeholders to store for history
            sql_query = result["sql_query"]
            df_preview = None
            summary = None
            figures = []

            # Show SQL query
            st.subheader("📝 Generated SQL Query")
            st.code(sql_query, language="sql")

            # Show extracted data
            project_root = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(project_root, "dataExtracted.csv")

            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                df_preview = df.head(20)

                st.subheader("📊 Extracted Data Preview")
                st.dataframe(df_preview)

                st.download_button(
                    label="⬇️ Download Extracted CSV",
                    data=open(csv_path, "rb"),
                    file_name="dataExtracted.csv",
                    mime="text/csv"
                )

                with st.spinner("📝 Summarizing extracted data..."):
                    summary = summarizeTable(csv_path)

                if summary:
                    st.subheader("📌 Summary")
                    st.write(summary)

                figures = plotGraphs("dataExtracted.csv")
                if figures:
                    st.subheader("📊 Visualization")
                    for fig in figures:
                        st.pyplot(fig)
                else:
                    st.warning("No valid plots generated.")
            else:
                st.error("CSV file not found after SQL execution.")

            # Save assistant response with results into history
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Here are your query results:",
                "summary": summary,
                "figures": figures
            })
        else:
            st.error("⚠️ Query failed or returned no results.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Query failed or returned no results."
            })
