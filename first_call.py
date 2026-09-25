import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

response=client.chat.completions.create(
    model="kimi-k3",
    messages=[{"role":"user", "content":"Hello, what model are you?"}],
)

print(response.choices[0].message.content)

print(response.usage)
