from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage
model = ChatTongyi(model="qwen-max")

messages = [
    SystemMessage(content="你是Python专家，简洁明了的回答问题"),
    HumanMessage(content="python print end和flush参数分别有什么用，简洁明了的回答。")
]

# for chunk in model.stream(messages):
#     print(chunk.content, end="", flush=True)
while messages and messages[-1].content != "exit()":
    res = model.stream(messages)
    for chunk in res:
        print(chunk.content, end="", flush=True)
    print()  # 换行
    user_input = input("请输入问题（输入exit()退出）：")
    messages=[HumanMessage(content=user_input)]
    