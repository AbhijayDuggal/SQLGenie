import os
import pandas as pd
import sqlite3
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from core.llm import GeminiLLM
from core.retrieval import SchemaRetriever
from core.prompts import build_prompt
from core.sql_executor import run_sql
from core.sql_validation import is_safe_sql

# --- Streamlit Page Config ---
st.set_page_config(page_title="SQL Generator", layout="wide")
st.markdown("<h1 style='text-align: center;'>SQL Genie</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>GEN AI BASED SQL GENERATOR</h4>", unsafe_allow_html=True)
st.write("") # Add a little space

# --- Step 1: Database selection ---
st.subheader("Choose your database")
use_default = st.checkbox("Use default sample database", value=True)
db_path = None

if not use_default:
    uploaded_file = st.file_uploader("Upload your SQLite database", type=["db", "sqlite"])
    if uploaded_file is not None:
        db_path = f"temp_{uploaded_file.name}"
        with open(db_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
else:
    db_path = "data/sample.db"
    if not os.path.exists(db_path):
        st.warning("Default database not found. Please upload your own database.")
        db_path = None

# --- Proceed if database is available ---
if db_path:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        if not tables:
            st.error("This database has no tables. Upload a valid SQLite database.")
            db_path = None
        else:
            st.success(f"Database loaded successfully! Found {len(tables)} table(s).")
            st.subheader("Tables and Columns")
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                cols = [col[1] for col in cursor.fetchall()]
                st.write(f"**{table}**: {', '.join(cols)}")
        conn.close()
    except Exception as e:
        st.error(f"Invalid database file: {e}")
        db_path = None

# --- Initialize LLM and SchemaRetriever ---
if db_path:
    # Initialize LLM once
    if "llm" not in st.session_state:
        st.session_state.llm = GeminiLLM()
    llm = st.session_state.llm

    # Initialize retriever only if database changed or not set
    if "retriever" not in st.session_state or st.session_state.retriever.db_path != db_path:
        st.session_state.retriever = SchemaRetriever(db_path)
    retriever = st.session_state.retriever

    # --- Step 2: Ask SQL Questions ---
    st.subheader("Ask your SQL question")
    query = st.text_input("Enter your question:")

    if st.button("Generate SQL") and query.strip():
        try:
            # Retrieve schema info dynamically
            schema_info = retriever.get_schema_info()

            # Build LLM prompt
            prompt = build_prompt(query, schema_info)

            # Generate SQL
            sql = llm.generate(prompt)

            # --- Clean up the SQL ---
            # Remove markdown blocks like ```sql ... ```
            if sql.startswith("```"):
                sql = sql.split("```")[-2].strip()
            # Remove leading 'sql' keyword if present
            elif sql.lower().startswith("sql"):
                sql = "\n".join(sql.splitlines()[1:]).strip()

            # Show generated SQL
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # Execute safely
            if is_safe_sql(sql):
                cols, rows = run_sql(db_path, sql)
                if rows:
                    st.subheader("Query Results")
                    df = pd.DataFrame(rows, columns=cols)
                    st.dataframe(df)
                else:
                    st.info("Query returned no results.")
            else:
                st.error("SQL failed safety check. Dangerous operations detected.")

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Please upload a valid database or ensure the default sample.db exists.")

footer_style = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117; /* Matches Streamlit dark mode bg */
    color: #808495; /* Subtle grey text */
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #262730; /* Thin border for separation */
    z-index: 1000;
}
</style>
<div class="footer">
    Developed by <b>Abhijay</b> and <b>Avni</b>
</div>
"""
st.markdown(footer_style, unsafe_allow_html=True)