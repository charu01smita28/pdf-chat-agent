from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

import asyncio

class EmbeddingService:
    def __init__(self, api_key: str, model: str):
        self._embeddings = OpenAIEmbeddings(api_key=api_key)
        self._model = ChatOpenAI(model=model, temperature=0)


    async def generate_embedding(self, text: str):
        # Simulate asynchronous embedding generation
        return await asyncio.to_thread(self._embeddings.embed_text, text)

    async def generate_embeddings(self, text_chunks: list[str]):
        # Asynchronously generate embeddings for all text chunks
        tasks = [self.generate_embedding(chunk) for chunk in text_chunks]
        return await asyncio.gather(*tasks)
    
    def generate_embedding(self, text: str):
        return self._embeddings.embed_query(text)
