from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set. Check your .env file.")

# Paths
pdf_path = Path(__file__).parent / "the-site-reliability-workbook-next18.pdf"

# Load PDF
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(documents=docs)

# Embeddings (use latest model name)
embedding_model = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",          # recommended new embedding model
    google_api_key=api_key               # <- force use of API key
)

# Store vectors in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="RAG_Based_ChatWithPDF"
)

print("Vector store created and documents added successfully.")
