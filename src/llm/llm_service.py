import json
from pydantic import ValidationError
from src.llm.client import extract_tasks_with_llm, repair_tasks_with_llm
from src.llm.parsing import parse_and_validate
from src.llm.quarantine import log_quarantine

def extract_validated_tasks(text):

    response = extract_tasks_with_llm(text)

    try:
        return parse_and_validate(response)
    except (json.JSONDecodeError, ValidationError) as error:

        new_response = repair_tasks_with_llm(text,response,str(error))

        try:
            return parse_and_validate(new_response)
        except (json.JSONDecodeError, ValidationError) as new_error:
            log_quarantine(text,new_response,new_error,"extract-tasks-v1")
            raise