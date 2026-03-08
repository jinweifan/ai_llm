from langchain_community.llms.tongyi import Tongyi

# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
model = Tongyi(model="qwen-max")

# 调用invoke向模型提问
res = model.invoke(input="你和其他模型的核心比较？以及核心优势，简洁明了的回答。")
print(res)

res = model.stream("python print end和flush参数分别有什么用，简洁明了的回答。")
for chunk in res:
    print(chunk, end="", flush=True)
