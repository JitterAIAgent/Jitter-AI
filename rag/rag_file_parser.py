import os
import tiktoken

def text_file_rag(rag_file_path: str) -> list:
    """Load RAG facts from a text file and chunk by max tokens from env."""
    if not os.path.exists(rag_file_path):
        raise FileNotFoundError(f"RAG file '{rag_file_path}' does not exist.")

    with open(rag_file_path, 'r', encoding='utf-8') as file:
        rag_facts = file.read().strip()

    if not rag_facts:
        return []

    # Get max tokens per chunk from env, default 256
    try:
        max_tokens = int(os.getenv("RAG_CHUNK_TOKENS", 256))
    except Exception:
        max_tokens = 256

    # Use tiktoken to tokenize and chunk
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(rag_facts)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks