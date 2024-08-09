from langchain_community.vectorstores import Chroma

import asyncio

class ChromaDBService:
    def __init__(self, path: str, embeddings):
        self._db = Chroma(collection_name="agent_collection", persist_directory=path, embedding_function=embeddings)

    async def upsert_embeddings(self, embeddings: list, text_chunks: list[str]):
        tasks = [self._upsert_embedding(i, embedding, text_chunk) for i, (embedding, text_chunk) in enumerate(zip(embeddings, text_chunks))]
        await asyncio.gather(*tasks)

    async def _upsert_embedding(self, index: int, embedding, text_chunk: str):
        await asyncio.to_thread(self._db.add_documents, [(str(index), {"embedding": embedding, "text": text_chunk})])

    def query(self, embedding, k=1):
        return self._db.query(embedding, k=k)

    def generate_retriever(self, documents, embeddings):
        """ Generate the Retriever class for VectorStore by loading the documents and creating the vector database """
        vectorstore = Chroma.from_documents(
            documents=documents,
            collection_name="rag-chroma",
            embedding=embeddings,
        )
        retriever = vectorstore.as_retriever()
        return retriever