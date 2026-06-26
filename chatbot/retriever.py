
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
VectorStoreIndex,
SimpleDirectoryReader,
)


documents = SimpleDirectoryReader(
"./chatbot/policies"
).load_data()

Settings.embed_model = HuggingFaceEmbedding(
model_name="BAAI/bge-small-en-v1.5"
)


index = VectorStoreIndex.from_documents(documents)

retriever = index.as_retriever(
similarity_top_k=3
)