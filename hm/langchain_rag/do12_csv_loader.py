from langchain_community.document_loaders import CSVLoader


loader = CSVLoader(file_path="hm/langchain_rag/info.csv", encoding="utf-8")
docs = loader.load()
print("document ", docs)
# print("document ", loader.lazy_load())  # 返回迭代器
for doc in loader.lazy_load():
    print(doc.page_content)
