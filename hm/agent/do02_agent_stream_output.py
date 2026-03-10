from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
import json


def to_dict(obj):
  """把含 LangChain Message 的 chunk 转成可 JSON 序列化的 dict。"""
  if hasattr(obj, 'model_dump'):
    return obj.model_dump()
  if hasattr(obj, 'dict'):
    return obj.dict()
  if isinstance(obj, dict):
    return {k: to_dict(v) for k, v in obj.items()}
  if isinstance(obj, list):
    return [to_dict(x) for x in obj]
  return obj


@tool(description="获取股票价格")
def get_price(name: str) -> str:
    return f"股票{name}的价格是100元"


@tool(description="获取股票信息")
def get_stock_info(name: str) -> str:
    return f"股票{name}，是一家上市公司，成立于2000年，是一家高科技公司，主要从事人工智能、大数据、云计算等业务。"


model = ChatTongyi(model="qwen-max")
agent = create_agent(model, tools=[get_price, get_stock_info], system_prompt="你是一个股票分析师，请根据用户的问题获取股票信息")
res = agent.stream({
    "messages": [
        {"role": "user", "content": "Figma股价是多少呢？ 以及Figma公司信息是什么？"}
    ]
}, stream_mode="values")
for chunk in res:
    # print(json.dumps(to_dict(chunk), indent=4, ensure_ascii=False))
    latest_message = chunk['messages'][-1]
    if latest_message.content:
        print(type(latest_message).__name__, ":", latest_message.content)
    
    try:
        if latest_message.tool_calls:
            print(f"工具调用：{[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError:
        pass
