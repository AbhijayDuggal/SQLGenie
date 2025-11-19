import sqlite3
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SchemaRetriever:
    def __init__(self, db_path):
        self.db_path = db_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.faiss_index = None
        self.schema_texts = []
        self.build_index()

    def get_schema_info(self):
        """Return list of schema strings from the database"""
        schema_info = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]

                for table in tables:
                    cursor.execute(f"PRAGMA table_info({table});")
                    cols = [col[1] for col in cursor.fetchall()]
                    schema_info.append(f"Table: {table}, Columns: {', '.join(cols)}")
        except Exception as e:
            print(f"[SchemaRetriever] Error reading schema: {e}")
        return schema_info

    def build_index(self):
        """Build FAISS index from schema info"""
        self.schema_texts = self.get_schema_info()
        if not self.schema_texts:
            print("[SchemaRetriever] No schema found to build FAISS index.")
            return

        embeddings = self.model.encode(self.schema_texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dim)
        self.faiss_index.add(embeddings.astype('float32'))

    def retrieve(self, query, top_k=3):
        """Retrieve top-k relevant schema info for a natural language query"""
        if not self.schema_texts or self.faiss_index is None:
            print("[SchemaRetriever] FAISS index not initialized. Returning all schema.")
            return self.schema_texts

        q_emb = self.model.encode([query], convert_to_numpy=True).astype('float32')
        D, I = self.faiss_index.search(q_emb, min(top_k, len(self.schema_texts)))
        return [self.schema_texts[i] for i in I[0]]
