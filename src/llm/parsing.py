import json
from src.llm.schema import ExtractTasksResponse

def parse_and_validate(raw_text):
    cleaned = raw_text.strip()

    lines = cleaned.splitlines()

    if len(lines) >= 3 and lines[0] in ("```json","```") and lines[-1] == "```":
        cleaned = "\n".join(lines[1:-1])

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        object_start = cleaned.find("{")

        if object_start == -1:
            raise

        decoder = json.JSONDecoder()
        parsed, object_end = decoder.raw_decode(cleaned, object_start)

        remaining = cleaned[object_end:].strip()

        if remaining not in ("", "```"):
            raise json.JSONDecodeError(
                "Unexpected content after the JSON object",
                cleaned,
                object_end,
            )

    return ExtractTasksResponse.model_validate(parsed)