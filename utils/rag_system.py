import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from parsers.parse_being_json import load_being_json

being = load_being_json()
knowledge_documents = being["knowledge"]
model = None
index = None

if knowledge_documents and knowledge_documents != []:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    document_embeddings = model.encode(knowledge_documents, convert_to_numpy=True)
    embedding_dimension = document_embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dimension)
    index.add(document_embeddings)

def get_rag_context(query: str, top_k: int = 3) -> str:
    if not knowledge_documents or not model or not index:
        return ""
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    retrieved_documents = [knowledge_documents[i] for i in indices[0]]
    context_string = "\n".join(retrieved_documents)
    return context_string

if __name__ == "__main__":
    print("\n--- RAG System Ready ---")
    user_query_1 = "how old is john"
    context_1 = get_rag_context(user_query_1, top_k=2)
    print(f"\nUser Query: '{user_query_1}'")
    print(context_1)