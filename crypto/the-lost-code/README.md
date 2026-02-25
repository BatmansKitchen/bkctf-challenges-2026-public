# The Lost Code

**Flag:** `bkctf{triangle_shaft_horse_yacht}`

## Overview

The challenge presented an image encoded in a custom variation of the [Pigpen cipher](https://en.wikipedia.org/wiki/Pigpen_cipher). The goal was to decode the plaintext and submit it as the flag.

## Encoding Scheme

The alphabet is split into 5 groups, each anchored by a vowel:
```
A: ABCD
E: EFGH
I: IJKLMN
O: OPQRST
U: UVWXYZ
```

Each letter is represented by its **group vowel** + an **offset** (0–5), where the offset is encoded visually by a symbol drawn around the letter's position:

| Offset | Symbol |
|--------|--------|
| 0 | Empty (nothing in middle) |
| 1 | Dot |
| 2 | `\` diagonal |
| 3 | `/` diagonal |
| 4 | Vertical line |
| 5 | Horizontal line |

For example, `BKCTF` encodes as `A2 I3 A3 O5 E0`.

## Solution

Decoding the image symbol by symbol:
```
O5 O3 I0 A0 I5 I3 E0 _  O4 E3 A0 E1 O5 _ E3 O0 O3 O4 E0 _ U4 A0 A2 O5
T  R  I  A  N  G  L  _  S  H  A  F  T  _  H  O  R  S  E  _  Y  A  C  T
```

Giving the plaintext: **triangle shaft horse yacht**

`bkctf{triangle_shaft_horse_yacht}`

Next year, I'll make one uncrackable by LLMs >:)