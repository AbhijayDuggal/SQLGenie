# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load your .env file
# load_dotenv()

# # Configure Gemini with your API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # List models
# models = genai.list_models(page_size=100)

# print("Available models:\n")
# for m in models:
#     print(m.name)


import sqlite3

conn = sqlite3.connect("data/sample.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees;")
rows = cursor.fetchall()
print(rows)
conn.close()