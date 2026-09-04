import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client= OpenAI(
    api_key=os.environ["MOONSHOOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

with open ("chart.jpg", "rb") as f:
     b64= base64.b64encode(f.read()).decode()

response= client.chat.completions.create(
     model="kimi-k3",
     messages=[{"role":"user", "content":[{
          "type":"text",
          "text": "When did the trend change, and by how much?"
     },
     {"type":"image_url",
      "image_url":{"url": 
                   f"data:image/jpeg;base64,{b64}"}}

     ]}]
)

print(response.choices[0].message.content)
