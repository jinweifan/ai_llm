from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_ollama import ChatOllama


chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        # ("system", "你是一个英雄联盟喷子，你需要用喷子的口吻回答问题，简洁明了的回答问题"),
        ("system", "你是直播行业的百事通，知晓所有的直播信息，也知道最近的直播资讯、名场面和热梗，简洁明了的回答问题"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
history_data = [
    # ("human", "李青怎么样？"),
    # ("assistant", "李青是个垃圾英雄，操作难度大，伤害低，根本不适合新手玩。"),
]
# model = ChatTongyi(model="qwen3-max")
model = ChatOllama(model="qwen3.5:cloud")
chain = chat_prompt_template | model
# res = chain.stream(input={"input": "你觉得英雄联盟哪个英雄最强？", "history": history_data})
it = input("请输入问题（输入exit()退出）：")
while it != "exit()":
    res = chain.stream(input={"input": it, "history": history_data})
    history_data.append(("human", it))
    answer_str= ''
    for chunk in res:
        print(chunk.content, end="", flush=True)
        if answer_str:
            answer_str += f"\n{chunk.content}"
        else:
            answer_str = str(chunk.content)
    print()  # 换行
    history_data.append(("assistant", answer_str))
    it = input("请输入问题（输入exit()退出）：")