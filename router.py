import os

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI, RateLimitError

load_dotenv()

client= OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

MODEL_CHEAP="kimi-k2.6"
MODEL_SMART="kimi-k3"

def pick_model(question):
    word_count=len(question.split())
    if word_count <=12:
        return MODEL_CHEAP
    return MODEL_SMART

def ask(question):
    model=pick_model(question)
    print(f"Routing to:{model}")
    return client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":question}],
)

def ask_with_fallback(question):
    model=pick_model(question)
    try:
        print(f"Trying:{model}")
        return client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":question}],
)
    except (RateLimitError, APIStatusError) as error:
        print(f"{model} failed ({error}). Falling back to {MODEL_CHEAP}")
        return client.chat.completions.create(
    model=MODEL_CHEAP,
    messages=[{"role":"user", "content":question}],
)


response1=ask("What is the capital of USA?")
print(response1.choices[0].message.content)

response2=ask("Design a multi-step agentic workflow that reads 200 page contract,"
            "extracts every payment clause, cross checks them against our internal,"
              "policy document, and flags any clause that needs legal review")

print(response2.choices[0].message.content)



