# SQLGenie
 Generative AI Based SQL Generator
SQL Genie — AI-Powered Natural Language to SQL Generator

SQL Genie uses Generative AI to convert natural language questions into SQL queries. It supports both SQLite and MySQL, retrieves schema context intelligently using embeddings + FAISS, validates SQL safety, executes queries (for SQLite), and provides interactive chat-style history.

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

Images:
<img width="975" height="441" alt="image" src="https://github.com/user-attachments/assets/32058e1b-f271-4150-a9ed-7613234f799a" />
<img width="975" height="437" alt="image" src="https://github.com/user-attachments/assets/b9c2d6a6-dbe3-458b-82f4-463c446ea7b1" />
<img width="975" height="403" alt="image" src="https://github.com/user-attachments/assets/7dab73f3-5c76-4cfc-947e-b55cae3fec7b" />
<img width="975" height="378" alt="image" src="https://github.com/user-attachments/assets/4f746b78-1289-4f48-b3f7-fa5bf415b5bb" />
<img width="975" height="383" alt="image" src="https://github.com/user-attachments/assets/1b26172e-2cfc-4eca-8fbb-931f21302a0b" />


