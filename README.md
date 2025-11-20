# SQLGenie
 Generative AI Based SQL Generator
SQL Genie — AI-Powered Natural Language to SQL Generator

SQL Genie is a Streamlit-based application that uses Generative AI to convert natural language questions into SQL queries. It supports both SQLite and MySQL, retrieves schema context intelligently using embeddings + FAISS, validates SQL safety, executes queries (for SQLite), and provides interactive chat-style history.

Features
1. Natural Language → SQL
Ask questions in plain English, and SQL Genie generates clean, optimized SQL for your database.

2. Dual Database Support
SQLite → Load .db / .sqlite files and execute SQL directly.
MySQL → Upload .sql dumps, retrieve schema, and generate SQL (execution handled externally).

3. Intelligent Schema Retrieval
Built-in SchemaRetriever:
Reads SQLite schema directly.
Parses MySQL schema from uploaded SQL file.
Embeds schema text using Sentence Transformers.
Uses FAISS for fast semantic search to improve SQL generation.

4. Chat-Based Memory
Your previous questions and SQL responses are preserved in a conversational flow, improving context and continuity.

5. SQL Safety Check
Dangerous operations such as DROP, DELETE, ALTER, TRUNCATE, etc., are blocked for protection.

6. Clean UI Built with Streamlit
Simple, responsive interface for uploading databases, asking questions, and viewing results.

Tech Stack:
Component	Technology
Frontend	Streamlit
LLM	Gemini API (via custom wrapper)
Embeddings	Sentence-Transformers (MiniLM-L6-v2)
Vector Search	FAISS
DB Support	SQLite, MySQL
SQL Execution	SQLite only
Environment	Python 3.10+



No destructive operations allowed
