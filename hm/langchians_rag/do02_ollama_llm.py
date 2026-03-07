from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:latest")
res = llm.invoke("你的详细信息是什么？")
print(res)