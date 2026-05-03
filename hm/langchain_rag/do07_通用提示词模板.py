from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template("What year did {name} win the world cup?")

prompt_text = prompt_template.format(name="Brazil")

model = Tongyi(model="qwen-max")

# res = model.invoke(prompt_text)
# print(res)

chain = prompt_template | model
res = chain.invoke(input={"name": "Brazil"})
print(res)