import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    client= OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",)
    
    response=client.chat.completions.create(
    model="kimi-k3",
    messages=[{"role":"system", "content":"You are a terse assistant. Answer in one sentence"},
        {"role":"user", "content":"Hello, my name is Abner"}],
        extra_body={"provider":{"order":["relace/fp4"], "allow_fallbacks": True}})
    reply1=response.choices[0].message.content
    print(reply1)
except KeyError:
    print("Missing MOONSHOT_API_KEY- Check .env file")
except Exception as e:
    print("Somethin went wrong:", e)   


response=client.chat.completions.create(
    model="kimi-k3",
    messages=[{"role":"system", "content":"You are a terse assistant. Answer in one sentence"},
              {"role":"assistant","content": reply1},
        {"role":"user", "content":"Hello, what is my name?"}],
)

print(response.choices[0].message.content)