import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client= OpenAI(
    api_key=os.environ["MOONSHOOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)


video= client.files.create(
    file=open("videoTest.mp4", "rb"), purpose="video")

response= client.chat.completions.create(
     model="kimi-k3",
     messages=[{"role":"user", "content":[{
          "type":"text",
          "text": "what happens in this video?"
     },
     {"type":"video_url",
      "video_url":{"url": 
                   f"ms://{video.id}"}}

     ]}]
)

print(response.choices[0].message.content)
