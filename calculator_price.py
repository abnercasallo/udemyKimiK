
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LONG_SYSTEM_PROMPT = """
You are a helpful assistant specialized in explaining large language model
architectures to software engineers. You should always answer with technical
precision, referencing Mixture-of-Experts routing, attention mechanisms, and
context window management where relevant. You should keep explanations under
five sentences unless the user explicitly asks for more depth. You should
never speculate about unreleased features and should clearly say when you are
uncertain about a technical detail.
""" * 30

client= OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

response=client.chat.completions.create(
    model="kimi-k3",
    messages=[{"role":"system", "content":LONG_SYSTEM_PROMPT},
        {"role":"user", "content":"who are you?"}
              ],
)


PRICE_INPUT=3.00/1_000_000
PRICE_OUTPUT=15.00/1_000_000
PRICE_CACHED=0.30/1_000_000

def get_cached_tokens(usage):
    if usage.prompt_tokens_details is None:
        return 0
    return usage.prompt_tokens_details.cached_tokens or 0

def calculate_cost(prompt_tokens, completions_tokens, cached_tokens=0):
    uncached_input=prompt_tokens-cached_tokens
    cost=(uncached_input*   PRICE_INPUT+
          cached_tokens* PRICE_CACHED
          + completions_tokens* PRICE_OUTPUT)
    return round(cost, 6) 

cached_tokens=get_cached_tokens(response.usage)

cost=calculate_cost(prompt_tokens=response.usage.prompt_tokens,
                    completions_tokens=response.usage.completion_tokens,
                    cached_tokens=cached_tokens)


print(response.choices[0].message.content)
print(f"Cost of this call: ${cost}")
print(f"Total Cashed Tokens: {cached_tokens}. It costs ${cached_tokens*PRICE_CACHED}")
print(response.usage)


    