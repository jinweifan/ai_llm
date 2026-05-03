import time
import streamlit as st

from knowledge_base import KnowledgeBaseService

st.title("文件上传")
uploaded_file = st.file_uploader("上传文件", type=["txt", "pdf", "docx", "doc", "csv", "xlsx", "xls"], accept_multiple_files=False)

if "counter" not in st.session_state:
    st.session_state["counter"] = 0
if "knowledge_base" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploaded_file:
    # st.success(f"文件{uploaded_file.name}上传成功")
    file_content = uploaded_file.read()
    size = uploaded_file.size / 1024 
    st.write(f"文件名：{uploaded_file.name}, 文件类型：{uploaded_file.type}, 文件大小：{size}KB")
    # st.write(uploaded_file.getvalue().decode("utf-8"))
    st.session_state["counter"] += 1
    service: KnowledgeBaseService = st.session_state["service"]
    
    with st.spinner("文件上传中..."):
        upload_status = service.upload_by_str(file_content.decode("utf-8"), uploaded_file.name)
        st.write(file_content.decode("utf-8"))
        time.sleep(1)
        if upload_status:
            st.success("文件上传成功")
        else:
            st.error("此文件已存在，请勿重复上传")
    

print("文件上传次数：", st.session_state["counter"])
    
