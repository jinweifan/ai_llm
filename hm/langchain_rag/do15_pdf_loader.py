from langchain_community.document_loaders import PyPDFLoader

# loader = PyPDFLoader("hm/langchain_rag/pdf1.pdf", mode="single")  # mode="single" 按页加载，mode="page" 按页加载，mode="element" 按元素加载
loader = PyPDFLoader("hm/langchain_rag/pdf2.pdf", password="itheima", mode="page")
docs = loader.lazy_load()
print("docs ", docs)
for i, doc in enumerate(docs):
    print("-" * 100)
    print(f"第{i+1}页：{doc}")
    print("-" * 100)    
