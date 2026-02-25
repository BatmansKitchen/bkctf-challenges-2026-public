#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHALLENGE_DIR = BASE_DIR / "challenge"
RUNTIME_DIR = CHALLENGE_DIR / ".runtime"
FLAG = os.environ.get("FLAG", "bkctf{test_flag}")

SUBMISSION_TEMPLATE = """
set_option warningAsError true

example (a b c n) : (a + 1) ^ (n + 3) + (b + 1) ^ (n + 3) ≠ (c + 1) ^ (n + 3) := """

def build_submission(args: str) -> str:
    return SUBMISSION_TEMPLATE + args


def main(submission_path, response):
    submission_file = CHALLENGE_DIR / submission_path

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    # with open(submission_file, 'w') as f:
        # f.write(build_submission(response))
    submission_file.write_text(build_submission(response), encoding="utf-8")

    proc = subprocess.run(
        ["lake", "env", "lean", str(submission_file)],
        cwd=str(CHALLENGE_DIR),
        text=True,
        capture_output=True,
        check=False,
    )

    if proc.returncode != 0:
        print(proc)
        return "Uh oh! Something went wrong. Unfortunately, we weren't able to figure out why, but maybe try to use live.lean-lang.org to figure out why?"
    
    return f"Congrats! You inputted correct code! Your flag is as follows: {FLAG}"


if __name__ == "__main__":
    raise SystemExit(main(RUNTIME_DIR / "Submission.lean"), input(SUBMISSION_TEMPLATE))
