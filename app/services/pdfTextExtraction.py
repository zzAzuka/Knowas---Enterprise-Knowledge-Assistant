from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from app.core.models import embeddings_ollama
import fitz
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DOWNLOAD_DIR = './filesFromBucket'
INDEX_NAME = "knowledge-assistant-vector-lake"

try:
    pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))
    index = pc.Index("knowledge-assistant-vector-lake")
except Exception as e:
    logging.critical(f"Failed to connect to Pinecone: {e}")

def cleanExtractedText(text):
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text

def chunkingText(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def embedChunks(chunks, filename):
    vectors = []
    embeddings = embeddings_ollama.embed_documents(chunks)
    
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": f"{filename}-chunk-{i}",
            "values": vector,
            "metadata": {"source": filename, "text": chunk}  
        })
    return vectors

def addToPinecone(vectors):
    index.upsert(vectors = vectors)

def pdfTextExtraction(filename: str) -> None:
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return

    logging.info(f"Extracting text from: {filename}")

    try:
        with fitz.open(filepath) as doc:
            extracted_text = "".join(page.get_text() for page in doc)
    except Exception as e:
        logging.error(f"Error reading PDF '{filename}': {e}")
        return

    if not extracted_text.strip():
        logging.warning(f"No text extracted from: {filename}")
        return

    cleaned_text = cleanExtractedText(extracted_text)
    chunks = chunkingText(cleaned_text)
    vectors = embedChunks(chunks, filename)
    addToPinecone(vectors)

    logging.info(f"Completed processing for: {filename}")