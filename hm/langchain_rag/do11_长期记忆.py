from typing import Sequence
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

import os
import json
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict

class FileChatMessageHistory(BaseChatMessageHistory):
    
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path + '.json', "r", encoding="utf-8") as f:
                messages_dict = json.load(f)
                return messages_from_dict(messages_dict)
        except FileNotFoundError:
            return []
        
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        messages_dict = messages_to_dict(all_messages)
        with open(self.file_path + '.json', "w", encoding="utf-8") as f:
            json.dump(messages_dict, f, ensure_ascii=False)

    def clear(self) -> None:
        self._messages = []
        with open(self.file_path + '.json', "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)


model = ChatTongyi(model="qwen3-max")
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题，对话历史：{chat_history}, 用户提问： {input}, 请回答"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题, 对话历史: "),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "请回答如下问题：{input}"),
    ]
)

str_parser = StrOutputParser()


def print_history(history):
    print("=" * 20 + history.to_string() + "=" * 20)
    return history


base_chain = prompt | print_history | model | str_parser

store = {}


def get_history(session_id):
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(session_id, "./chat_history")
    return store[session_id]


history = RunnableWithMessageHistory(
    base_chain,  #  被增强的原有链
    get_history,
    input_message_key="input",
    history_messages_key="chat_history",
)

def stream_print(resp):
    for chunk in resp:
        print(chunk, end="", flush=True)
    print()

if __name__ == "__main__":
    session_config = RunnableConfig(configurable={"session_id": "user_001"})
    # history_chain = history.stream(input={"input": "小明有3本书"}, config=session_config)
    # stream_print(history_chain)
    # history_chain = history.stream(input={"input": "小红有2本书"}, config=session_config)
    # stream_print(history_chain)
    # history_chain = history.stream(input={"input": "小李有5本书"}, config=session_config)
    # stream_print(history_chain)
    history_chain = history.stream(input={"input": "我烧了10本书"}, config=session_config)
    stream_print(history_chain)
    history_chain = history.stream(
        input={"input": "一共有多少本书？"}, config=session_config
    )
    stream_print(history_chain)