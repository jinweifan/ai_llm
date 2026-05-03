from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

prompt_template = PromptTemplate.from_template(
    "小明今天花了{money}元，他爸爸挣了{salay}元，请问小明家今天净收入入多少钱？（仅输出净收入金额，不要其他内容）"
)
second_prompt_template = PromptTemplate.from_template(
    "小明家今天目前净收入{amount}元，但他妈妈又买菜花了{price}元， 请问小明家今天净收入多少钱？"
)
# second_prompt_template.format(price=100)

model = ChatTongyi(model="qwen3-max")
str_parser = StrOutputParser()
# json_parser = JsonOutputParser()
lambda_func = RunnableLambda(lambda a: {"amount": a.content, "price": 50})
chain = prompt_template | model
for chunk in chain.stream({"money": 100, "salay": 3000}):
    print(chunk.content, end="", flush=True)
print()
chain = chain | lambda_func | second_prompt_template | model | str_parser
# 完整链的入口仍是 prompt_template，需要 money、salay；amount/price 由 lambda_func 提供
for chunk in chain.stream({"money": 100, "salay": 3000}):
    print(chunk, end="", flush=True)
