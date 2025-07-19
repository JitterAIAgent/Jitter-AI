import os
import sys

from dotenv import load_dotenv

from rag.rag_file_parser import text_file_rag
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
import faiss

load_dotenv()

USE_FILE_RAG = os.getenv("USE_FILE_RAG", "True").lower() == "true"

def file_rag():
    """
    Loop through the 'files' folder and parse each .txt file using text_file_rag.
    Returns a dict mapping filename (without extension) to its RAG content.
    """
    files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
    rag_contents = {}
    if not os.path.exists(files_dir):
        print(f"[file_rag] Directory '{files_dir}' does not exist.")
        return rag_contents
    for filename in os.listdir(files_dir):
        try:
            if filename.endswith('.txt'):
                file_path = os.path.join(files_dir, filename)
                chunks = text_file_rag(file_path)
                base_name = os.path.splitext(filename)[0]
                if isinstance(chunks, list):
                    for idx, chunk in enumerate(chunks):
                        # Use base_name_chunkN as key for each chunk
                        rag_contents[f"{base_name}_chunk{idx+1}"] = chunk
                else:
                    rag_contents[base_name] = chunks
            if filename.endswith('.pdf'):
                # If you want to handle PDF files, you can add logic here
                pass
        except Exception as e:
            print(f"[file_rag] Error reading {filename}: {e}")
    return rag_contents

if USE_FILE_RAG:
    rag_files = file_rag()
else:
    rag_files = {}

def get_index_model(being):
    knowledge_documents = being["knowledge"] + list(rag_files.values())
    
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
    knowledge_documents = being["knowledge"] + list(rag_files.values())
    if not knowledge_documents or not model or not index:
        return ""
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    retrieved_documents = [knowledge_documents[i] for i in indices[0]]
    context_string = "\n".join(retrieved_documents)
    return context_string
