from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

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
        store[session_id] = InMemoryChatMessageHistory()
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
    history_chain = history.stream(input={"input": "小明有3本书"}, config=session_config)
    stream_print(history_chain)
    history_chain = history.stream(input={"input": "小红有2本书"}, config=session_config)
    stream_print(history_chain)
    history_chain = history.stream(input={"input": "小刚有4本书"}, config=session_config)
    stream_print(history_chain)
    history_chain = history.stream(
        input={"input": "小明、小红、小刚一共有多少本书？"}, config=session_config
    )
    stream_print(history_chain)
