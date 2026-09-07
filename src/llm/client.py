from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

LLM_BASE_URL= os.getenv("LLM_BASE_URL")
LLM_API_KEY= os.getenv("LLM_API_KEY")
LLM_MODEL= os.getenv("LLM_MODEL")

client = OpenAI(api_key=LLM_API_KEY,base_url=LLM_BASE_URL)

project_root = Path(__file__).resolve().parents[2]

prompt_path = project_root / "prompts" / "extract-tasks-v1.md"

system_prompt = prompt_path.read_text(encoding="utf-8")

def extract_tasks_with_llm(text):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    temperature=0
)

    return response.choices[0].message.content


def repair_tasks_with_llm(text, broken_output, validation_error):

    instructions = f"""
    Your previous answer was rejected for this reason:
    {validation_error}

    Return only corrected JSON matching the schema in the system instructions.
    Do not include explanations or Markdown code fences.
    """

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
            {"role": "assistant", "content": broken_output},
            {"role": "user", "content": instructions},
        ]
    
    response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    temperature=0
)
    
    return response.choices[0].message.content
    
