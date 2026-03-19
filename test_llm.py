from llm.llm_client import LLMClient

client = LLMClient()

response = client.generate("Say hello in 1 line")

print(response)