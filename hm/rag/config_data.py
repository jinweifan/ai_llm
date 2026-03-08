from langchain_core.runnables import RunnableConfig


md5_path = "hm/rag/data/md5.txt"
collection_name = "knowledge_base"
persist_directory = "hm/rag/data/chroma_db"

embedding_model = "text-embedding-v4"

chunk_size = 100
chunk_overlap = 20
separators = ["\n\n", "\n", " ", "", "。", "，", "！", "？", "：", "；", "。", ".", "!", "?", ":", ";"]
max_chat_length = 2

similarity_threshold = 3
model = "qwen3-max"
chat_history_path = "hm/rag/data/chat_history"

session_config = RunnableConfig(configurable={"session_id": "user_001"})