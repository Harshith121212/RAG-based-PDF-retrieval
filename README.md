**📄 RAG-based PDF Retrieval App**

This project allows users to chat with a large PDF and get accurate answers retrieved from the document itself. The PDF is automatically split into chunks, embedded, and stored inside a Qdrant vector database. User queries are answered using Gemini, grounded strictly on the retrieved PDF content.

**🚀 Features**

Upload and process large PDF files, 
Automatic text splitting & chunking using LangChain, 
Store embeddings inside Qdrant, 
Query the PDF using a chat interface, 
Gemini provides answers based on retrieved chunks only, 
Each answer also returns the page number where the information appears, 

**🛠️ Tech Stack**

Python, 
LangChain, 
Qdrant Vector DB, 
Google Gemini (OpenAI-compatible API), 
PyPDFLoader for PDF extraction.

**📦 How It Works**

1. Load PDF using PyPDFLoader

2. Split content using RecursiveCharacterTextSplitter

3. Generate embeddings with GoogleGenerativeAIEmbeddings

4. Store vectors in Qdrant

At query time:

5. User question → vector search in Qdrant

6. Retrieve top matching chunks

Pass context to Gemini

Gemini answers using only PDF data

Page number reference included
