#!/usr/bin/env python3
from pwn import *
import re

MODULUS = 1999
URL  = 'localhost'
PORT = 1999

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def crack_lcg(sequence, modulus):
    x1, x2, x3 = sequence[0], sequence[1], sequence[2]

    numerator = (x3 - x2) % modulus
    denominator = (x2 - x1) % modulus

    denom_inv = mod_inverse(denominator, modulus)
    if denom_inv is None:
        raise ValueError("Modular inverse does not exist")

    a = (numerator * denom_inv) % modulus
    c = (x2 - a * x1) % modulus

    return a, c

def predict_next(sequence, a, c, modulus, count=5):
    current = sequence[-1]
    predictions = []

    for _ in range(count):
        current = (a * current + c) % modulus
        predictions.append(current)

    return predictions

def solve():
    # Connect using pwntools remote with SSL
    io = remote(
        URL,
        PORT,
        ssl=True
    )

    # Receive until we see the sequence
    data = io.recvuntil(b"comma-separated", timeout=10)
    response = data.decode()

    # Extract the 5-number sequence
    match = re.search(r'\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]', response)
    if not match:
        log.failure("Could not parse sequence")
        print(response)
        io.close()
        return

    sequence = [int(match.group(i)) for i in range(1, 6)]
    log.success(f"Sequence: {sequence}")

    # Crack LCG
    a, c = crack_lcg(sequence, MODULUS)
    log.success(f"Recovered parameters: a={a}, c={c}, m={MODULUS}")

    predictions = predict_next(sequence, a, c, MODULUS, 5)
    log.success(f"Predicted next 5 numbers: {predictions}")

    # Send answer
    answer = ",".join(map(str, predictions))
    io.sendline(answer.encode())

    # Receive final response
    result = io.recvall(timeout=5).decode()
    print("\n" + "="*60)
    print(result)
    print("="*60)

    # Extract flag if present
    flag_match = re.search(r'(bkctf|flag)\{[^}]+\}', result)
    if flag_match:
        log.success(f"FLAG: {flag_match.group(0)}")

    io.close()

if __name__ == "__main__":
    solve()
