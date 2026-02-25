#!/usr/bin/env python3
from pwn import *
import re
import math

NUM_SHOWN   = 8
NUM_PREDICT = 5

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

def recover_modulus(outputs):
    diffs = [outputs[i+1] - outputs[i] for i in range(len(outputs) - 1)]
    acc = 0
    for i in range(len(diffs) - 1):
        for j in range(i + 1, len(diffs) - 1):
            val = abs(diffs[i+1] * diffs[j] - diffs[j+1] * diffs[i])
            if val > 0:
                acc = math.gcd(acc, val)
    return acc if acc > 1 else None

def recover_lcg_params(outputs, modulus):
    s0, s1, s2 = outputs[0], outputs[1], outputs[2]
    denom_inv = mod_inverse((s1 - s0) % modulus, modulus)
    if denom_inv is None:
        return None, None
    a = ((s2 - s1) * denom_inv) % modulus
    c = (s1 - a * s0) % modulus
    return a, c

def predict_next(last_state, a, c, modulus, count=5):
    predictions = []
    state = last_state
    for _ in range(count):
        state = (a * state + c) % modulus
        predictions.append(state)
    return predictions

# Fun fact: This was my first time cracking an LCG in ANY ctf.
def solve():
    # Connect using pwntools remote with SSL
    io = remote(URL, PORT, ssl=True)

    # Receive until we see the sequence
    data = io.recvuntil(b"comma-separated", timeout=10)
    response = data.decode()

    # Extract the 8-number sequence
    match = re.search(r'\[(\d+(?:,\s*\d+){7})\]', response)
    if not match:
        log.failure("Could not parse sequence")
        print(response)
        io.close()
        return

    outputs = [int(x.strip()) for x in match.group(1).split(',')]
    log.success(f"Outputs: {outputs}")

    # recover modulus
    modulus = recover_modulus(outputs)
    if modulus is None:
        log.failure("Modulus recovery failed.")
        io.close()
        return
    log.success(f"Recovered modulus: {modulus}")

    # recover a and c
    a, c = recover_lcg_params(outputs, modulus)
    if a is None:
        log.failure("Parameter recovery failed.")
        io.close()
        return
    log.success(f"Recovered a={a}, c={c}")

    # predict next 5 full states
    predictions = predict_next(outputs[-1], a, c, modulus, NUM_PREDICT)
    log.success(f"Predictions: {predictions}")

    # send answer
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