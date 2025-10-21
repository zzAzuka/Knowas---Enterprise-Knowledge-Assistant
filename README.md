# Knowas: Enterprise-Knowledge-Assistant

This project is a **FastAPI-based backend application** designed for intelligent document processing and question-answering. It integrates **AWS S3**, **Pinecone**, and **LLMs** to create a complete backend pipeline for uploading, storing, embedding, and querying PDF-based knowledge sources.

---

## 🚀 Features

- **📁 Document Upload & Storage**
  - Upload PDF files via the `/upload` endpoint.
  - Files are securely stored in **AWS S3** for static storage.
  - The application uses **PyMuPDF** to extract text from the uploaded PDFs.

- **🧠 Vectorization & Retrieval**
  - Extracted text is transformed into **vector embeddings**.
  - Embeddings are stored and managed in a **Pinecone Vector Database** for semantic search and retrieval.
  - The `/query` endpoint allows users to ask questions, which are matched against document embeddings to fetch relevant chunks.

- **🤖 LLM-powered Answers**
  - Retrieved document chunks are passed to an **LLM** to generate accurate and context-aware responses to user queries.

- **🔐 Secure Endpoints**
  - Implements **JWT-based authentication** for all endpoints.
  - Upload access is restricted to **admin users**, whose credentials are managed in a dummy user database.

- **🐳 Dockerized Deployment**
  - The app includes a **Dockerfile** with complete build and run instructions.
  - Easily deploy the backend as a containerized service.

- **📊 MLflow Logging**
  - Integrated **MLflow tracking** to log intermediate outputs, such as extracted text, vectorization summaries, and LLM responses, for observability and debugging.

---

## ⚙️ Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Storage** | [AWS S3](https://aws.amazon.com/s3/) |
| **Vector Database** | [Pinecone](https://www.pinecone.io/) |
| **Text Extraction** | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) |
| **Logging** | [MLflow](https://mlflow.org/) |
| **Authentication** | JSON Web Tokens (JWT) |
| **Containerization** | Docker |

---

## 🧩 API Endpoints

### `/upload` – Upload a PDF Document  
**Method:** `POST`  
**Auth Required:** ✅ Admin Only  
**Description:**  
- Accepts a PDF file from the UI.  
- Extracts text using PyMuPDF.  
- Converts text to vector embeddings.  
- Stores both the file (in S3) and embeddings (in Pinecone).  

---

### `/query` – Query the Knowledge Base  
**Method:** `POST`  
**Auth Required:** ✅  
**Description:**  
- Accepts a question string.  
- Searches Pinecone for the most relevant text chunks.  
- Generates a final answer using an LLM.  

---

## 🔒 Authentication

- The app uses **JWT tokens** for secure access control.
- Admin users can upload documents, while general users can only query.
- Dummy user credentials are stored in a temporary in-memory database (or `.json`/`.db` file depending on configuration).

---
