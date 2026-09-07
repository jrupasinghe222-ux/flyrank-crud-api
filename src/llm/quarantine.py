import json
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

log_path = project_root / "logs" / "quarantine.jsonl"

def log_quarantine(text, raw_output, error, prompt_version):

    record = {
        "input":text,
        "output":raw_output,
        "error":str(error),
        "prompt_version":prompt_version
    }

    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(record) + "\n")