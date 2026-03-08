import time
import streamlit as st
from rag import RagService
import config_data as config

st.title("智能客服")
st.divider()

prompt = st.chat_input()

if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': '你好，我是智能客服，有什么可以帮你的吗？'}]

if "rag" not in st.session_state:
    st.session_state.rag = RagService()

if st.session_state.messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
else:
    st.chat_message("assistant").write("你好，我是智能客服，有什么可以帮你的吗？")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    ai_res_lt = list()
    def write_stream(response):
        for chunk in response:
            ai_res_lt.append(chunk)
            yield chunk
            
    with st.spinner("思考中..."):
        rag_service = st.session_state.rag
        response = rag_service.chain.stream({"input": prompt}, config=config.session_config)
        st.chat_message("assistant").write_stream(write_stream(response))
    st.session_state.messages.append({"role": "assistant", "content": "".join(ai_res_lt)})
    # response = rag_service.chain.invoke({"input": prompt}, config=session_config)
    # st.session_state.messages.append({"role": "assistant", "content": response})
