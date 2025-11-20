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
st.set_page_config(page_title="SQL Genie", layout="wide")
st.markdown("<h1 style='text-align: center;'>SQL Genie</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>GEN AI BASED SQL GENERATOR</h4>", unsafe_allow_html=True)
st.write("")

# --- Step 1: Database selection ---
st.subheader("Choose your database")
use_default = st.checkbox("Use default sample database", value=True)
db_path = None
db_type = "sqlite"  # Default type
mysql_config = {}

if not use_default:
    uploaded_file = st.file_uploader("Upload your database", type=["db", "sqlite", "sql"])
    if uploaded_file is not None:
        db_path = f"temp_{uploaded_file.name}"
        with open(db_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Detect type by extension
        if uploaded_file.name.endswith(".sql"):
            db_type = "mysql"
        else:
            db_type = "sqlite"
else:
    db_path = "data/sample.db"
    if not os.path.exists(db_path):
        st.warning("Default database not found. Please upload your own database.")
        db_path = None
    else:
        db_type = "sqlite"

# --- MySQL credentials input ---
if db_type == "mysql":
    st.subheader("MySQL Connection Details")
    mysql_config['host'] = st.text_input("Host", value="localhost")
    mysql_config['user'] = st.text_input("User", value="root")
    mysql_config['password'] = st.text_input("Password", type="password")
    mysql_config['database'] = st.text_input("Database name")
    if not all(mysql_config.values()):
        st.info("Please fill in all MySQL connection details.")
        db_path = None

# --- Proceed if database is available ---
if db_path:
    try:
        tables = []
        if db_type == "sqlite":
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
        elif db_type == "mysql":
            import mysql.connector
            conn = mysql.connector.connect(
                host=mysql_config['host'],
                user=mysql_config['user'],
                password=mysql_config['password'],
                database=mysql_config['database']
            )
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()

        if not tables:
            st.error("This database has no tables. Upload a valid database.")
            db_path = None
        else:
            st.success(f"Database loaded successfully! Found {len(tables)} table(s).")
            st.subheader("Tables and Columns")
            for table in tables:
                if db_type == "sqlite":
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute(f"PRAGMA table_info({table});")
                    cols = [col[1] for col in cursor.fetchall()]
                    conn.close()
                elif db_type == "mysql":
                    import mysql.connector
                    conn = mysql.connector.connect(
                        host=mysql_config['host'],
                        user=mysql_config['user'],
                        password=mysql_config['password'],
                        database=mysql_config['database']
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"SHOW COLUMNS FROM {table};")
                    cols = [row[0] for row in cursor.fetchall()]
                    conn.close()
                st.write(f"**{table}**: {', '.join(cols)}")

    except Exception as e:
        st.error(f"Invalid database file: {e}")
        db_path = None

# --- Initialize LLM, Retriever, and Chat History ---
if db_path:
    if "llm" not in st.session_state:
        st.session_state.llm = GeminiLLM()
    llm = st.session_state.llm

    if "retriever" not in st.session_state or getattr(st.session_state.retriever, 'db_path', None) != db_path:
        st.session_state.retriever = SchemaRetriever(db_path, db_type=db_type, mysql_config=mysql_config)
    retriever = st.session_state.retriever

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Step 2: Ask SQL Questions ---
    st.subheader("Ask your SQL question")
    query = st.text_input("Enter your question:")

    # Display conversation history
    if st.session_state.chat_history:
        st.subheader("Conversation History")
        for role, msg in st.session_state.chat_history:
            st.markdown(f"**{role}:** {msg}")

    # Generate SQL
    if st.button("Generate SQL") and query.strip():
        try:
            st.session_state.chat_history.append(("User", query))
            schema_info = retriever.get_schema_info()

            # Build prompt with database type
            prompt = build_prompt(
                query=query,
                schema_info=schema_info,
                chat_history=st.session_state.chat_history,
                db_type=db_type
            )

            sql = llm.generate(prompt)

            # Cleanup
            if sql.startswith("```"):
                sql = sql.split("```")[-2].strip()
            elif sql.lower().startswith("sql"):
                sql = "\n".join(sql.splitlines()[1:]).strip()

            st.session_state.chat_history.append(("Assistant", sql))
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            if db_type == "sqlite":
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
            else:
                st.info("MySQL detected: Execute the generated SQL on your MySQL server manually.")

        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Clear Conversation"):
        st.session_state.chat_history = []

else:
    st.info("Please upload a valid database or ensure the default sample.db exists.")

# --- Footer ---
footer_style = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: #808495;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #262730;
    z-index: 1000;
}
</style>
<div class="footer">
    Developed by <b>Abhijay</b> and <b>Avni</b>
</div>
"""
st.markdown(footer_style, unsafe_allow_html=True)
