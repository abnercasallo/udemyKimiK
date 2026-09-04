import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI(
    api_key=os.environ["MOONSHOOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

response=client.chat.completions.create(
    model="kimi-k3",
    reasoning_effort="max",
    messages=[{"role":"user", "content":"You drive 90 km to a meeting at 45 km/h, and drive back the same road at 90 km/h. What was your average speed for the whole trip?"}],
)

print(response.choices[0].message.content)
print("reasoning tokens:", response.usage.completion_tokens_details.reasoning_tokens)