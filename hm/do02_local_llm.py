from openai import OpenAI
import os

client = OpenAI(
    # 本地 Ollama 不校验 key，传占位符满足客户端校验即可
    api_key=os.getenv("OPENAI_API_KEY", "ollama"),

    base_url="http://localhost:11434/v1",
)

messages = [{"role": "user", "content": "你的详细信息是什么？"}]
completion = client.chat.completions.create(
    # model="qwen2.5:latest",  # 您可以按需更换为其它深度思考模型
    model="deepseek-r1:8b",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)