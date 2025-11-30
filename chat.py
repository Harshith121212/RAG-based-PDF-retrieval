from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set. Check your .env file.")


embedding_model = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
    google_api_key=api_key
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="RAG_Based_ChatWithPDF",
    embedding=embedding_model
)

##Taking user imput

user_input = input("Please enter your question about the PDF document: ")

search_results = vector_db.similarity_search(query=user_input)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = """
You are a helpful AI assistant that provides answers based on the content of a PDF document along with page_contents and page_number

You should only answer the user based on the context provided from the PDF document and navigate the user to open the right page number to know more"

Context:
{context}
"""
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
)

print("AI Assistant Response:", response.choices[0].message.content)
