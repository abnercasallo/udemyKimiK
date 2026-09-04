import os
import re
import time

import requests
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()  

client = OpenAI(
    base_url="https://api.moonshot.ai/v1", 
    api_key=os.environ["MOONSHOT_API_KEY"],
)

GOAL = "Brief me on Mixture-of-Experts in 5 bullets for a busy manager."
TOKEN_BUDGET = 15000 

SYSTEM = (
    "You are a research agent. You work toward the GOAL by choosing ONE action "
    "per turn, replying with exactly one line:\n"
    "SEARCH <query> — search Wikipedia\n"
    "READ <title> — read a full article\n"
    "DONE <the brief> — finish with the final answer\n"
    "No other text. Plan before you spend."
)

HEADERS = {"User-Agent": "kimi-k3-course-demo/1.0"}  


def ask_kimi(messages):  
    for attempt in range(3):
        try:
            return client.chat.completions.create(
                model="kimi-k3",  
                messages=messages,
            )
        except RateLimitError:
            print(f"  rate limit — waiting 20s (retry {attempt + 1}/3)")
            time.sleep(20)
    raise SystemExit("rate limit persists — try again later")


def search(query): 
    r = requests.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query", "list": "search", "srsearch": query,
        "format": "json", "srlimit": 3}, headers=HEADERS, timeout=10)
    #https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=mixture%20of%20experts&format=json&srlimit=3
    hits = r.json()["query"]["search"]
    return "\n".join(
        f'- {h["title"]}: {re.sub(r"<[^>]+>", "", h["snippet"])}' for h in hits
    )


def read(title):  
    r = requests.get(
        f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
        headers=HEADERS, timeout=10)
    return r.json().get("extract", "Article not found.")[:1500]


messages = [
    {"role": "system", "content": SYSTEM},
    {"role": "user", "content": f"GOAL: {GOAL}"},
]

spent = 0
for step in range(1, 9):  
    r = ask_kimi(messages)  
    spent += r.usage.prompt_tokens + r.usage.completion_tokens
    action = r.choices[0].message.content.strip()
    if not action:  
        action = "(empty reply)"
    print(f"step {step} | spent {spent}/{TOKEN_BUDGET} | {action[:60]}")

    if spent > TOKEN_BUDGET:
        print("BUDGET EXHAUSTED — stopping")
        break
    if action.startswith("DONE"):
        print("\n" + action[5:].strip())
        break
    if action.startswith("SEARCH"):
        result = search(action[7:])
    elif action.startswith("READ"):
        result = read(action[5:])
    else:
        result = "Invalid action — reply with SEARCH, READ or DONE."
    messages += [{"role": "assistant", "content": action},
                 {"role": "user", "content": f"Result:\n{result[:2000]}"}]