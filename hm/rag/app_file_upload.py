import streamlit as st

st.title("文件上传")
uploaded_file = st.file_uploader("上传文件", type=["txt", "pdf", "docx", "doc", "csv", "xlsx", "xls"], accept_multiple_files=False)
if uploaded_file:
    st.success(f"文件{uploaded_file.name}上传成功")
    file_content = uploaded_file.read()
    size = uploaded_file.size / 1024 
    st.write(f"文件名：{uploaded_file.name}, 文件类型：{uploaded_file.type}, 文件大小：{size}KB")
    st.write(file_content.decode("utf-8"))
    
