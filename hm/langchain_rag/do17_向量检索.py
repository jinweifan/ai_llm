from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough



model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题。请参考以下参考文档：{context}"),
        ("human", "请回答如下问题：{input}"),
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))
vector_store.add_texts(
    [
        "减肥就是少吃多动，保持良好的生活习惯",
        "在减脂的过程中，要控制饮食，增加运动量，保持良好的生活习惯",
        "减肥是一个长期的过程，需要坚持不懈，不要轻易放弃",
    ]
)
input_text = "怎么减肥？"

# query_docs = vector_store.similarity_search(input_text, k=3)
retriever = vector_store.as_retriever()

def print_prompt(prompt: ChatPromptTemplate):
    print("=" * 20 + prompt.to_string() + "=" * 20)
    return prompt

def format_func(docs: list[Document]):
    if not docs:
        return "无参考资料"
    context = "["
    for doc in docs:
        context += doc.page_content
    context += "]"
    return context

chain = {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
res = chain.invoke(input_text)
print(res)
