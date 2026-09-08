import json
import time
from pathlib import Path

import httpx


cases_path = Path(__file__).parent / "cases.json"
cases = json.loads(cases_path.read_text(encoding="utf-8"))

passed = 0

for number, case in enumerate(cases, start=1):
    print(f"\nCase {number}: {case['text']}")

    try:
        response = httpx.post(
            "http://localhost:8000/extract_tasks",
            json={"text": case["text"]},
            timeout=180.0,
        )

        if response.status_code != 200:
            print(f"FAIL: HTTP {response.status_code}")
            print(response.text)

        else:
            actual = response.json()
            expected = case["expected"]

            if actual == expected:
                print("PASS")
                passed += 1

            else:
                print("FAIL: Answer did not match")
                print("Expected:", expected)
                print("Actual:  ", actual)

    except httpx.RequestError as error:
        print(f"FAIL: Request error — {type(error).__name__}")

    except ValueError:
        print("FAIL: Response was not valid JSON")

    if number < len(cases):
        time.sleep(4)

total = len(cases)
percentage = passed / total * 100

print(f"\nExact-match score: {passed}/{total} ({percentage:.1f}%)")