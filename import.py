import openai
client = openai.OpenAI(
    api_key="sk-SCZUYySlDfvTNl0yU4eLzQ",
    base_url="<your_proxy_base_url>" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo", # model to send to the proxy
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ]
)

print(response)