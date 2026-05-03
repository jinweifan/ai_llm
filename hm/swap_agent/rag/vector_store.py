import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.config_handler import chroma_conf
from utils.file_handler import (
    csv_loader,
    get_file_md5_hex,
    list_dir_with_allowed_type,
    pdf_loader,
    text_loader,
)
from utils.path_tools import get_abs_path
from utils.logger_handler import logger
from model.factory import embedding_model


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_conf["persist_directory"],
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_documents(self):
        def check_md5_hex(md5_for_check: str) -> bool:
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip() == md5_for_check:
                        return True
            return False

        def save_md5_hex(md5_hex: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_hex + "\n")

        def get_file_documents(read_path: str) -> list[Document]:
            if read_path.endswith(".txt"):
                return text_loader(read_path)
            elif read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            elif read_path.endswith(".csv"):
                return csv_loader(read_path)
            else:
                return []

        allowed_file_type = tuple(chroma_conf["allow_knowledge_file_type"])
        for file_path in list_dir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]), allowed_file_type
        ):
            md5_hex = get_file_md5_hex(file_path)
            if check_md5_hex(md5_hex):
                logger.warning("[加载知识库]%s已存在", file_path)
                continue
            try:
                documents = get_file_documents(file_path)
                if documents:
                    for idx, document in enumerate(documents, start=1):
                        if not document:
                            logger.warning(
                                "[加载知识库]%s内第%d/%d文档无内容，跳过",
                                file_path,
                                idx,
                                len(documents),
                            )
                            continue
                        
                        split_documents = self.splitter.split_documents(documents)
                        if not split_documents:
                            logger.warning(
                                "[加载知识库]%s第%d/%d文档分片后，无有效内容，跳过",
                                file_path,
                                idx,
                                len(documents),
                            )
                            continue
                        
                        self.vector_store.add_documents(split_documents)
                        save_md5_hex(md5_hex)
                        logger.info("[加载知识库]%s第%d/%d文档加载完成", file_path, idx, len(documents))
            except Exception as e:
                # exc_info=True 会打印异常堆栈信息
                logger.error("[加载知识库]%s加载失败: %s", file_path, str(e), exc_info=True)
                continue


if __name__ == "__main__":
    vector_store_service = VectorStoreService()
    vector_store_service.load_documents()
    
    retriever = vector_store_service.get_retriever()
    results = retriever.invoke("扫拖一体机器人可以只扫地不拖地吗？")
    for result in results:
        print(result.page_content)
        print("-" * 50)
