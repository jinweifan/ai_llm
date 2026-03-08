from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("hm/langchain_rag/Python基础语法.txt", encoding="utf-8")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 每个chunk的最大长度
    chunk_overlap=50, # 每个chunk的重叠长度
    separators=["\n\n", "\n", " ", "", "。", "，", "！", "？", "：", "；"],  # 分隔符
    length_function=len # 长度函数
)
splits = splitter.split_documents(docs)
print("splits ", len(splits))
for split in splits:
    print("-" * 100)
    print(split.page_content)
    print("-" * 100)
