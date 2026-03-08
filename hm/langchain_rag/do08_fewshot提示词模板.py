from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example_template = PromptTemplate.from_template("单词: {word}, 反义词: {antonym}")

example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "高", "antonym": "矮"},
    {"word": "快", "antonym": "慢"},
    {"word": "上", "antonym": "下"},
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    prefix="请根据以下单词和反义词的例子，给出单词反义词。",
    suffix="单词: {input}, 反义词: ",
    input_variables=["input"],
)
model = Tongyi(model="qwen-max")
chain = few_shot_prompt | model
res = chain.stream(input={"input": "左"})
for chunk in res:
    print(chunk, end="", flush=True)