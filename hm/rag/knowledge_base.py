"""知识库"""


import hashlib
import os
from datetime import datetime

import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def check_md5(md5_str: str):
    """检查文件的md5值"""
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w", encoding="utf-8").close()
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            if line.strip() == md5_str:
                return True
    return False


def save_md5(md5_str: str):
    """保存文件的md5值"""
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_string_md5(content: str, encoding: str = "utf-8") -> str:
    """获取字符串的md5值"""
    return hashlib.md5(content.encode(encoding)).hexdigest()


class KnowledgeBaseService:
    
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model=config.embedding_model),
            persist_directory=config.persist_directory
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 每个chunk的最大长度
            chunk_overlap=config.chunk_overlap,  # 每个chunk的重叠长度
            length_function=len,  # 长度函数
            separators=config.separators,  # 分隔符
        )
    
    def upload_by_str(self, data: str, file_name: str):
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return False
        
        if len(data) > config.max_chat_length:
            docs: list[str] = self.spliter.split_text(data)
        else:
            docs = [data]

        metadata = {
            "source": file_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "user",
        }
        self.chroma.add_texts(docs, metadatas=[metadata for _ in range(len(docs))])
        save_md5(md5_hex)
        return True


if __name__ == "__main__":
    knowledge_base = KnowledgeBaseService()
    flag = knowledge_base.upload_by_str("Hello, World2!", "test_str.txt")
    print(flag)