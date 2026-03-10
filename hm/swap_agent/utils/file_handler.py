"""文件处理"""

import hashlib
import os
from utils.logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_core.documents import Document


def get_file_md5_hex(filepath: str) -> str:
    """获取字符串的md5值"""
    if not os.path.exists(filepath):
        logger.error("[MD5计算]文件不存在: %s", filepath)
        return None

    if not os.path.isfile(filepath):
        logger.error("[MD5计算]文件不是文件: %s", filepath)
        return None

    chunk_size = 4096  # 每次读取4096字节, 避免内存占用过大
    md5_obj = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
    except Exception as e:
        logger.error("[MD5计算]文件读取失败: %s, filepath: %s", str(e), filepath)
        return None
    return md5_obj.hexdigest()


def list_dir_with_allowed_type(path: str, allowed_types: tuple[str]) -> list[str]:
    """列出目录下所有允许类型的文件"""

    if not os.path.isdir(path):
        logger.error("[文件列表]目录不是目录: %s", path)
        return []

    return tuple(os.path.join(path, f) for f in os.listdir(path) if f.endswith(allowed_types))


def pdf_loader(filepath: str, password: str = None) -> list[Document]:
    """加载PDF文件"""
    loader = PyPDFLoader(filepath, password=password)
    return loader.load()


def text_loader(filepath: str) -> list[Document]:
    """加载文本文件"""
    loader = TextLoader(filepath, encoding="utf-8")
    return loader.load()


def csv_loader(filepath: str) -> list[Document]:
    """加载CSV文件"""
    loader = CSVLoader(filepath)
    return loader.load()
