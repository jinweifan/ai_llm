import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoresService:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": config.similarity_threshold}
        )

    def search(self, query: str, k: int = config.similarity_threshold):
        return self.vector_store.similarity_search(query, k=k)

    def add_texts(self, texts: list[str], metadata: list[dict]):
        return self.vector_store.add_texts(texts, metadata=metadata)

    def delete(self, ids: list[str]):
        return self.vector_store.delete(ids=ids)

if __name__ == "__main__":
    embeddings = DashScopeEmbeddings(model=config.embedding_model)
    vector_stores = VectorStoresService(embeddings)
    retriever = vector_stores.get_retriever()
    print(retriever.invoke("我的体重180斤， 尺码推荐"))
    # print(vector_stores.search("什么是Python？"))
    # print(vector_stores.add_texts(["什么是Python？"], [{"source": "Python"}]))
    # print(vector_stores.delete(["1"]))