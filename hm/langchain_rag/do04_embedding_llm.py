from langchain_community.embeddings import DashScopeEmbeddings

embed = DashScopeEmbeddings()
# res = embed.invoke("你是谁？")

print(embed.embed_query("你是谁？"))
print(embed.embed_documents(["你是谁？", "你是干什么的？"]))