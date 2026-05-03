from langchain_core.tools import tool
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import (
    before_agent,
    after_agent,
    before_model,
    after_model,
    wrap_model_call,
    wrap_tool_call,
)
from langgraph.runtime import Runtime
from langchain_community.chat_models.tongyi import ChatTongyi

@tool(description="获取天气")
def get_weather() -> str:
    return "晴天"


@before_agent
def log_before_agent(state: AgentState, runtime: Runtime):
    print("before_agent")


@after_agent
def log_after_agent(state: AgentState, runtime: Runtime):
    print("after_agent")


@before_model
def log_before_model(state: AgentState, runtime: Runtime):
    print("before_model")

@after_model
def log_after_model(state: AgentState,  runtime: Runtime):
    print("after_model")


@wrap_model_call
def log_wrap_model_call(request, handler):
    print("wrap_model_call")
    return handler(request)

@wrap_tool_call
def log_wrap_tool_call(request, handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行参数：{request.tool_call['args']}")
    return handler(request)


model = ChatTongyi(model="qwen-max")
agent = create_agent(
    model,
    tools=[get_weather],
    system_prompt="你是一个天气预报员，请根据用户的问题获取天气",
    middleware=[
        log_before_agent,
        log_after_agent,
        log_before_model,
        log_after_model,
        log_wrap_model_call,
        log_wrap_tool_call,
    ],
)
res = agent.stream({
    "messages": [
        {"role": "user", "content": "今天北京天气怎么样？"}
    ]
}, stream_mode="values")
for chunk in res:
    print(chunk)