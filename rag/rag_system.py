import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def get_index_model(being):
    knowledge_documents = being["knowledge"]
    model = None
    index = None

    if knowledge_documents and knowledge_documents != []:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        document_embeddings = model.encode(knowledge_documents, convert_to_numpy=True)
        embedding_dimension = document_embeddings.shape[1]
        index = faiss.IndexFlatL2(embedding_dimension)
        index.add(document_embeddings)

        print("\n--- RAG System Ready ---")

    return model, index


def get_rag_context(being, model, index, query: str, top_k: int = 3) -> str:
    knowledge_documents = being["knowledge"]
    if not knowledge_documents or not model or not index:
        return ""
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    retrieved_documents = [knowledge_documents[i] for i in indices[0]]
    context_string = "\n".join(retrieved_documents)
    return context_string
