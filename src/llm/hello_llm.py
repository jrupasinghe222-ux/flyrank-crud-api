from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

LLM_BASE_URL= os.getenv("LLM_BASE_URL")
LLM_API_KEY= os.getenv("LLM_API_KEY")
LLM_MODEL= os.getenv("LLM_MODEL")

client = OpenAI(api_key=LLM_API_KEY,base_url=LLM_BASE_URL)

response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[{"role": "user", "content": "Reply with exactly the word: ready"}]
)

print(response.choices[0].message.content)