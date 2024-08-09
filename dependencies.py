from agents.services.embedding_service import EmbeddingService
from agents.services.chromadb_service import ChromaDBService
from agents.services.pdf_loader import PDFLoaderService
from agents.services.chat_agent import ChatAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")

# Initialize services globally
pdf_loader_service = PDFLoaderService()
embedding_service = EmbeddingService(api_key=OPENAI_API_KEY, model=OPEN_AI_MODEL)
chroma_db_service = ChromaDBService(path=CHROMA_DB_PATH, embeddings=embedding_service)

# Initialize ChatAgent
chat_agent = ChatAgent(
    pdf_loader_service=pdf_loader_service,
    embeddings_service=embedding_service,
    vector_db_service=chroma_db_service
)

def get_pdf_loader_service():
    return pdf_loader_service

def get_embedding_service():
    return embedding_service

def get_chroma_db_service():
    return chroma_db_service

def get_chat_agent():
    return chat_agent
