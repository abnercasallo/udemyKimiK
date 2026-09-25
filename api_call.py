import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    client= OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",)
    
    response=client.chat.completions.create(
    model="kimi-k3",
    messages=[{"role":"system", "content":"You are a terse assistant. Answer in one sentence"},
        {"role":"user", "content":"Hello, my name is Abner"}],)
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

#1.System: Instructions
#2.User: What the human says
#3.Assistant: What the MODEL already said