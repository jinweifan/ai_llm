"""RAG服务"""


from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.logger_handler import logger
from utils.prompt_loader import load_rag_prompt
from model.factory import chat_model
from rag.vector_store import VectorStoreService


def print_prompt(prompt: str):
    print("-" * 50)
    print(prompt.to_string())
    print("-" * 50)
    return prompt


class RAGSummaryService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.chat_model = chat_model
        self.prompt_template = PromptTemplate.from_template(
            self.prompt_text
        )
        self.chain = self.__init_chain()
        
    def __init_chain(self):
        chain = self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        # 检索相关文档
        context_docs: list[Document] = self.retriever_docs(query)
        
        # 拼接参考资料
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】 ：参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
        
        return self.chain.invoke({
            "input": query,
            "context": context
        })


if __name__ == "__main__":
    rag_summary_service = RAGSummaryService()
    result = rag_summary_service.rag_summarize("小户型适合哪些扫地机器人")
    print(result)
