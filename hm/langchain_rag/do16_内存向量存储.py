from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="info",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="hm/langchain_rag/chroma_db"
)

# vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())
# loader = CSVLoader(file_path="hm/langchain_rag/info.csv", encoding="utf-8", source_column="source")  # source_column 指定源文件的列名
# docs = loader.load()
# print("docs ", docs)
# vector_store.add_documents(docs, ids=[str(i) for i in range(1, len(docs) + 1)])

# vector_store.delete(ids=[1,2])

# query_docs = vector_store.similarity_search("Python好学吗？", key=3)
query_docs = vector_store.similarity_search("Python好学吗？", k=3, filter={"source": "黑马程序员"})
print("query_docs ", query_docs)
print("query_docs_len ", len(query_docs))
