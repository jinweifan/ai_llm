
from langchain_ollama import OllamaEmbeddings

embed = OllamaEmbeddings(model="qwen3-embedding")
print(embed.embed_query("你是谁？"))
print(embed.embed_documents(["你是谁？", "你是干什么的？"]))