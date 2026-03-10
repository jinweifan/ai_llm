from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取天气")
def get_weather(city: str) -> str:
    return "晴天"


model = ChatTongyi(model="qwen-max")

agent = create_agent(model, tools=[get_weather], system_prompt="你是一个天气预报员，请根据用户的问题获取天气")
res = agent.invoke({
    "messages": [
        {"role": "user", "content": "今天北京天气怎么样？"}
    ]
})
for msg in res["messages"]:
    print(type(msg).__name__, ":", msg.content)








