# AuraDocs - Document QA Bot

A Retrieval Augmented Generation (RAG) application that allows users to upload a PDF and ask questions about its contents.

## Features

- Upload a PDF document
- Extract and chunk PDF text
- Generate semantic embeddings using Sentence Transformers
- Store and search embeddings using FAISS
- Retrieve relevant sections using MMR search
- Generate answers using the Groq API
- Support basic conversational interactions

## How It Works

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
Sentence Transformer Embeddings
 ↓
FAISS Vector Search
 ↓
User Question
 ↓
Relevant Chunks Retrieved
 ↓
Groq LLM
 ↓
Answer
```

## Tech Stack
- Python
- Streamlit
- LangChain
- PyMuPDF
- Sentence Transformers
- FAISS
- Groq API

## Live Demo

[Open AuraDocs](https://auradocs-ag.streamlit.app/)
