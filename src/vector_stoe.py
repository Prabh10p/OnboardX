# app/ai/vector_store.py

import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Tuple


class VectorStore:
    """
    Simple FAISS-based vector memory to store conversation history
    or previous onboarding-related responses.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.text_data = []
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def add_text(self, text: str):
        """Convert text to embedding and add to FAISS index."""
        vector = self.embedding_model.embed_query(text)
        vector_np = np.array([vector]).astype("float32")
        self.index.add(vector_np)
        self.text_data.append(text)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Search for top-k similar text entries in history."""
        query_vec = np.array([self.embedding_model.embed_query(query)]).astype("float32")
        D, I = self.index.search(query_vec, top_k)
        results = [(self.text_data[i], float(D[0][idx])) for idx, i in enumerate(I[0]) if i < len(self.text_data)]
        return results

    def get_all(self):
        """Retrieve all stored text snippets."""
        return self.text_data
