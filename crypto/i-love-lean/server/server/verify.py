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

def mem_effecient_mod_exp (b e m c : Nat) : Nat :=
    if e > 0 then
      mem_effecient_mod_exp b (e - 1) m ((b * c) % m)
    else
      c % m

theorem it_works (b e m : Nat) : mem_effecient_mod_exp b e m 1 = (b ^ e) % m := """

def build_submission_lines(args: str) -> list[str]:
    return (SUBMISSION_TEMPLATE + args).splitlines(keepends=True)

def main(submission_path, response):
    submission_file = CHALLENGE_DIR / submission_path

    submission_file.parent.mkdir(parents=True, exist_ok=True)
    lines = build_submission_lines(response)
    with open(submission_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)

    proc = subprocess.run(
        ["lake", "env", "lean", str(submission_file)],
        cwd=str(CHALLENGE_DIR),
        text=True,
        capture_output=True,
        check=False,
    )

    if proc.returncode != 0:
        return "Uh oh! Something went wrong. Unfortunately, we weren't able to figure out why, but maybe try to use live.lean-lang.org to figure out why?"
    
    return f"Congrats! You inputted correct code! Your flag is as follows: {FLAG}"


if __name__ == "__main__":
    raise SystemExit(main(RUNTIME_DIR / "Submission.lean"), input(SUBMISSION_TEMPLATE))
