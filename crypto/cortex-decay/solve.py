from math import prod


def int_to_bytes(x: int) -> bytes:
    if x == 0:
        return b"\x00"
    return x.to_bytes((x.bit_length() + 7) // 8, "big")


def main() -> None:
    c = 40732687938760268194816992508783308058844901710443215136378413744389173154801
    e = 65537
    n = 67000000000000000000000000245061662851489575612371642903203727663237160203426

    # We get these from https://factordb.com/index.php?query=67000000000000000000000000245061662851489575612371642903203727663237160203426
    factors = [
        2,
        3,
        67,
        1483,
        14180303,
        40938258341,
        1324437742957822811,
        146170986161787706448601731202221987,
    ]

    n_from_factors = prod(factors)
    if n_from_factors != n:
        raise ValueError(
            f"Provided factors do not multiply to n.\n"
            f"  got: {n_from_factors}\n"
            f"  exp: {n}"
        )

    phi = prod(p - 1 for p in factors)
    d = pow(e, -1, phi)

    m = pow(c, d, n)
    m_bytes = int_to_bytes(m)

    print(f"n         = {n}")
    print(f"phi(n)    = {phi}")
    print(f"d         = {d}")
    print(f"m (int)   = {m}")
    print(f"m (bytes) = {m_bytes!r}")
    try:
        print(f"m (utf-8) = {m_bytes.decode()}")
    except UnicodeDecodeError:
        print("m (utf-8) = <not valid UTF-8>")


if __name__ == "__main__":
    main()