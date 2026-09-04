import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODELS = {  # $/1M tokens 
    "moonshotai/kimi-k3":       {"in": 3.0,  "out": 15.0},
    "openai/gpt-5.5":           {"in": 5.0,  "out": 30.0},
    "anthropic/claude-fable-5": {"in": 10.0, "out": 50.0},
}

doc = Path("spec.txt").read_text()

PROMPTS = [
    f"Summarize this 40-page spec in 5 bullets:\n\n{doc}",
    "Write a Python retry decorator with exponential backoff",
]

def run_benchmark(prompts, models):
    rows = []
    for prompt in prompts:
        for name, price in models.items():
            t0 = time.time()
            r = client.chat.completions.create(
                model=name,
                messages=[{"role": "user", "content": prompt}],
            )  # NO pasar temperature/top_p: K3 los rechaza
            dt = time.time() - t0
            u = r.usage
            cost = u.prompt_tokens * price["in"] / 1e6 \
                 + u.completion_tokens * price["out"] / 1e6
            rows.append({"model": name, "sec": round(dt, 1),
                         "cost": round(cost, 4),
                         "text": r.choices[0].message.content})
    return rows

if __name__ == "__main__":
    rows = run_benchmark(PROMPTS, MODELS)

    print(f"\n{'MODEL':28s} {'SEC':>7s} {'COST $':>9s}")  # summary table
    print("-" * 46)
    for r in rows:
        print(f"{r['model']:28s} {r['sec']:>7.1f} {r['cost']:>9.4f}")

    for r in rows:  # full responses for side-by-side quality review
        print(f"\n===== {r['model']} =====")
        print(r["text"])