from dotenv import load_dotenv
import os
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

load_dotenv()

# Configure Gemini as the global LLM and embedding model BEFORE importing pdf
api_key = os.environ.get("GEMINI_API_KEY", "").strip()
Settings.llm = GoogleGenAI(model="gemini-2.0-flash", api_key=api_key)
Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-2", api_key=api_key)
