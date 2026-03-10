import time
import streamlit as st
from agent.tools.react_agent import ReactAgent

st.title("扫地机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    resp_list = []
    with st.spinner("思考中..."):
        st.session_state.agent.execute_stream(prompt)
        
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                time.sleep(0.01)
                yield chunk
            
        st.chat_message("assistant").write_stream(capture(st.session_state.agent.execute_stream(prompt), resp_list))
        st.session_state.messages.append({"role": "assistant", "content": resp_list[-1]})
        st.rerun()
        # for chunk in resp_list:
        #     st.chat_message("assistant").write(chunk)
        #     st.session_state.messages.append({"role": "assistant", "content": [-1]})