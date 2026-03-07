from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatTongyi(model="qwen3-max", api_key=None)
messages = [
    SystemMessage(content="你是一个英雄联盟喷子，你需要用喷子的口吻回答问题，简洁明了的回答问题"),
]

resp = model.stream(messages + [HumanMessage(content="你觉得英雄联盟哪个英雄最强？")])
for chunk in resp:
    print(chunk.content, end="", flush=True)
