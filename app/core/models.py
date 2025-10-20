import os
from langchain_ollama import OllamaEmbeddings, ChatOllama

embeddings_ollama = OllamaEmbeddings(model="nomic-embed-text")
model_ollama = ChatOllama(model="gemma3:4b", temperature=0.4)