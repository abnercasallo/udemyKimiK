import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI(
    api_key=os.environ["MOONSHOOT_API_KEY"],
    base_url="https://api.moonshot.ai/v1",
)

REPO= Path("starter_repo")
TASK="Make the tests pass. The cart and the invoice disagree about the total"

SYSTEM=("You are a coding agent. You recieve a whole repo and a task"
        "Reply with the COMPLETE new content of every file you change,"
        "each starting with a line: ###<relative path>. No explanations")

def load_repo(repo):
    return "\n\n".join(f"###{p.relative_to(repo)}\n{p.read_text()}"
                       for p in sorted(repo.rglob("*.py")))

def apply_edits(text):
    for block in text.split("###")[1:]:
        path,content= block.split("\n",1)
    (REPO/path.strip()).write_text(content.strip()+"\n")
    print(f"edited:{path.strip()}")


def run_tests():
    r=subprocess.run(["python", "-m", "pytest", "-x", "-q"], capture_output=True,
                     text=True, cwd=REPO) #python -m pytest -x -q
    return  r.returncode, r.stdout + r.stderr

messages=[{"role": "system", "content": SYSTEM},
          {"role": "user", "content": f"Repo:\n{load_repo(REPO)} \n\nTask: {TASK}"}]

for step in range (1,4):
    r= client.chat.completions.create( model="kimi-k3",
                                      messages= messages )
    reply= r.choices[0].message.content
    print(f"step {step}- {r.usage.prompt_tokens} tokens in")
    apply_edits(reply)
    code,output= run_tests()
    if code==0:
        print(f"step {step}: TESTS PASS")
        break
    print(f"step{step}: tests fail- feeding erros back")
    messages+=[{"role":"assistant", "content": reply},
               {"role": "user", "content": f"Tests failed: \n {output[-2000:]}"}]





