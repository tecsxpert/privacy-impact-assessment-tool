import chromadb
from chromadb.utils import embedding_functions
import os

class VectorStore:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "chroma_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(
            name="privacy_knowledge",
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents, metadatas, ids):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text, n_results=3):
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

vector_store = VectorStore()
