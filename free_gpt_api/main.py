from client import get_gpt_response

messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

result = get_gpt_response(messages)
print(result)  # Should print: "The capital of France is Paris." or similar
