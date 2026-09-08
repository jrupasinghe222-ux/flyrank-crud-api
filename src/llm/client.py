from pathlib import Path
from dotenv import load_dotenv
import os
import random
import time
import json
from openai import OpenAI, APITimeoutError, APIStatusError
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

load_dotenv()

LLM_BASE_URL= os.getenv("LLM_BASE_URL")
LLM_API_KEY= os.getenv("LLM_API_KEY")
LLM_MODEL= os.getenv("LLM_MODEL")

client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
    timeout=30.0,
    max_retries=0
    )

project_root = Path(__file__).resolve().parents[2]

prompt_path = project_root / "prompts" / "extract-tasks-v1.md"

system_prompt = prompt_path.read_text(encoding="utf-8")

def parse_retry_after(value):
    if value is None:
        return None

    value = value.strip()

    if value.isascii() and value.isdigit():
        return int(value)

    try:
        retry_time = parsedate_to_datetime(value)

        if retry_time.tzinfo is None:
            retry_time = retry_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delay = (retry_time - now).total_seconds()

        return max(0.0, delay)

    except (ValueError, TypeError, OverflowError):
        return None

def complete_with_retry(messages,  is_repair=False):
    for attempt in range(2):
        
        delay = None
        response = None

        started_at = time.perf_counter()

        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                temperature=0,
            )

            return response.choices[0].message.content

        except APITimeoutError:
            if attempt == 1:
                raise

        except APIStatusError as error:
            retryable = (error.status_code == 429 or 500 <= error.status_code < 600)

            if not retryable or attempt == 1:
                raise

            if error.status_code == 429:
                retry_after = error.response.headers.get("Retry-After")
                delay = parse_retry_after(retry_after)

                if delay is not None and delay > 5:
                    raise
        finally:
            duration_ms = round( (time.perf_counter() - started_at) * 1000,2,)
            usage = getattr(response, "usage", None)
            input_tokens = getattr(usage, "prompt_tokens", None)
            output_tokens = getattr(usage, "completion_tokens", None)
            actual_model = getattr(response, "model", None) or LLM_MODEL

            record = {
            "event": "llm_call",
            "prompt_version": prompt_path.stem,
            "model": actual_model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "duration_ms": duration_ms,
            "attempt": attempt + 1,
            "is_repair": is_repair,
            "repair_count": int(is_repair),
            "response_received": response is not None,
            }

            print(json.dumps(record), flush=True)

        if delay is None:
            delay = (2 ** attempt) + random.uniform(0, 0.5)

        time.sleep(delay)
    

def extract_tasks_with_llm(text):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    return complete_with_retry(messages)


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

    
    return complete_with_retry(messages, is_repair=True)
    
