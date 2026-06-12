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

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pdf import sri_lanka_engine
from note_engine import note_engine

tools = [
    note_engine,
    QueryEngineTool(
        query_engine=sri_lanka_engine,
        metadata=ToolMetadata(
            name="sri_lanka_data",
            description="this gives detailed information about Sri Lanka the country, including its history, geography, culture, economy, and people",
        ),
    ),
]

import asyncio

agent = ReActAgent(
    tools=tools,
    llm=Settings.llm,
    verbose=True,
    system_prompt="Purpose: The primary role of this agent is to assist users by providing accurate information about Sri Lanka.",
)

async def main():
    while (prompt := input("Enter a prompt (q to quit): ")) != "q":
        result = await agent.run(prompt)
        print(result)

asyncio.run(main())
