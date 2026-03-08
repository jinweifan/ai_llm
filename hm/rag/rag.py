

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory
from file_history_store import get_history
from vector_stores import VectorStoresService
import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


class RagService:
    
    def __init__(self):
        self.vector_stores = VectorStoresService(DashScopeEmbeddings(model=config.embedding_model))
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "你需要根据会话历史回应用户问题。请参考以下参考文档：\n{context}"),
                ("system", "并且我提供用户的对话历史：\n"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "请回答如下问题：{input}"),
            ]
        )
        self.chat_model = ChatTongyi(model=config.model)
        self.chain = self.__get_chain()
        
    def format_func(self, docs: list[Document]):
        if not docs:
            return "无参考资料"
        format_str = ""
        for doc in docs:
            format_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
        return format_str

    def print_prompt(self, prompt: ChatPromptTemplate):
        print("=" * 20 + prompt.to_string() + "=" * 20)
        return prompt

    def __get_chain(self):
        def extra_input(data: dict):
            return data['input']
        
        def extra_data(data: dict):
            data['history'] = data['input']['history']
            data['input'] = data['input']['input']
            return data
        
        dt = {
            "input": RunnablePassthrough(),
            "context": extra_input | self.vector_stores.get_retriever() | self.format_func,
        }
        
        chain = dt | RunnableLambda(extra_data) | self.prompt_template  | self.print_prompt | self.chat_model | StrOutputParser()
        chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_message_key="input",
            history_messages_key="history",
        )
        return chain

if __name__ == "__main__":
    session_config = RunnableConfig(configurable={"session_id": "user_001"})
    rag_service = RagService()
    res = rag_service.chain.invoke({"input": "春天穿什么衣服呢？"}, config=session_config)
    print(res)
