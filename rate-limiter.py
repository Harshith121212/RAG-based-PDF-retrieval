from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI, APIError
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
import time

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

# --- 2. DEFINE THE RATE LIMITING LOGIC ---
@retry(
    retry=retry_if_exception_type(APIError), 
    wait=wait_random_exponential(multiplier=1, max=10), 
    stop=stop_after_attempt(5) 
)
def get_chat_response(messages):
    return client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )

# --- 3. MAIN CHAT LOOP ---
print("------------------------------------------------")
print("Chat Session Started. Type 'exit' to quit.")
print("------------------------------------------------")

while True:
    user_input = input("\nYour Question: ")
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting...")
        break

    try:
        # Search Qdrant
        search_results = vector_db.similarity_search(query=user_input)
        
        context = "\n\n".join([
            f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page_label', 'N/A')}\nFile Location: {result.metadata.get('source', 'N/A')}" 
            for result in search_results
        ])

        # Prepare messages
        formatted_prompt = SYSTEM_PROMPT.format(context=context)
        messages = [
            {"role": "system", "content": formatted_prompt},
            {"role": "user", "content": user_input}
        ]

        # Call the function
        print("Thinking...")
        response = get_chat_response(messages)
        
        print("\nAI Assistant Response:", response.choices[0].message.content)
        
        
        time.sleep(2) 

    except Exception as e:
        print(f"\n❌ Error: {e}")

