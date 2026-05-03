from langchain_community.document_loaders import JSONLoader
import json
loader = JSONLoader(file_path="hm/langchain_rag/stu.json", jq_schema=".", text_content=False)
docs = loader.load()
print("document ", docs)
for doc in docs:
    print(json.loads(doc.page_content))
    
loader = JSONLoader(file_path="hm/langchain_rag/stu.json", jq_schema=".other.addr")
docs = loader.load()
print("other.address ", docs)
# for doc in docs:
#     print(json.loads(doc.page_content))

loader = JSONLoader(file_path="hm/langchain_rag/stus.json", jq_schema=".[].name")
docs = loader.load()
print("names ", docs)
for doc in docs:
    print(doc.page_content)
    
loader = JSONLoader(file_path="hm/langchain_rag/stu_json_lines.json", jq_schema=".", text_content=False, json_lines=True)
docs = loader.load()
print("json_lines ", docs)
for doc in docs:
    print(json.loads(doc.page_content))
