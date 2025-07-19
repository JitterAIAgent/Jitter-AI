import csv
import re
from bs4 import BeautifulSoup
import PyPDF2
import os
import tiktoken

max_tokens = None

try:
    max_tokens = int(os.getenv("RAG_CHUNK_TOKENS", 256))
except Exception:
        max_tokens = 256

# === Plain Text File Parser ===
def text_file_rag(rag_file_path: str) -> list:
    """Load RAG facts from a text file and chunk by max tokens from env."""
    if not os.path.exists(rag_file_path):
        raise FileNotFoundError(f"RAG file '{rag_file_path}' does not exist.")

    with open(rag_file_path, 'r', encoding='utf-8') as file:
        rag_facts = file.read().strip()

    if not rag_facts:
        return []

    # Use tiktoken to tokenize and chunk
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(rag_facts)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

# === PDF File Parser ===
def pdf_file_rag(pdf_file_path: str) -> list:
    """Load RAG facts from a PDF file and chunk by max tokens from env."""
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"RAG file '{pdf_file_path}' does not exist.")

    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
        pdf_text = pdf_text.strip()

    if not pdf_text:
        return []

    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(pdf_text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

# === HTML File Parser ===
def html_file_rag(html_file_path: str) -> list:
    """Load RAG facts from an HTML file and chunk by max tokens from env."""
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"RAG file '{html_file_path}' does not exist.")

    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Use BeautifulSoup to extract visible text
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)

    if not text:
        return []

    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks
# === CSV File Parser ===
def csv_file_rag(csv_file_path: str) -> list:
    """Load RAG facts from a CSV file and chunk by max tokens from env."""
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"RAG file '{csv_file_path}' does not exist.")

    rows = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Join all columns in the row with a space
            rows.append(' '.join([str(cell) for cell in row if cell]))
    csv_text = '\n'.join(rows).strip()
    if not csv_text:
        return []
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(csv_text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

# === Markdown File Parser ===
def md_file_rag(md_file_path: str) -> list:
    """Load RAG facts from a Markdown file and chunk by max tokens from env."""
    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"RAG file '{md_file_path}' does not exist.")

    with open(md_file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # Remove code blocks and inline code
    md_content = re.sub(r'```[\s\S]*?```', '', md_content)  # Remove fenced code blocks
    md_content = re.sub(r'`[^`]*`', '', md_content)  # Remove inline code
    # Remove markdown links/images, keep visible text
    md_content = re.sub(r'!\[[^\]]*\]\([^\)]*\)', '', md_content)  # Remove images
    md_content = re.sub(r'\[[^\]]*\]\([^\)]*\)', lambda m: m.group(0).split(']')[0][1:], md_content)  # Keep link text
    # Remove markdown headings, formatting
    md_content = re.sub(r'^#+\s*', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'[*_#>-]', '', md_content)
    text = md_content.strip()
    if not text:
        return []
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks