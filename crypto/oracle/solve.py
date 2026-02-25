from pwn import remote
import re

BLOCK_SIZE = 16
HOST = "gotham-microsystems-02f755c67557a26a.instancer.batmans.kitchen"
PORT = 1337

class PaddingOracle:
    def __init__(self):
        self._connect()

    def _connect(self):
        try:
            self.conn.close()
        except Exception:
            pass

        self.conn = remote(HOST, PORT, ssl=True)
        banner = self.conn.recvuntil(b"> ")

        m = re.search(rb"\(([0-9A-F]+)\)", banner)
        if not m:
            raise Exception("Failed to extract ciphertext")

        self.ciphertext = bytes.fromhex(m.group(1).decode())
        print(f"Ciphertext blocks: {len(self.ciphertext) // BLOCK_SIZE}")

    def query(self, ct: bytes) -> bool:
        try:
            self.conn.sendline(ct.hex().upper().encode())
            resp = self.conn.recvuntil(b"> ", timeout=2)
        except KeyboardInterrupt:
            raise
        except Exception:
            self._connect()
            return self.query(ct)

        if b"Bad Padding" in resp:
            return False
        if b"Invalid API Key" in resp or b"Nice try" in resp:
            return True

        return False

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass


def split_blocks(data):
    return [data[i:i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]


def recover_block(oracle, blocks, index, is_last=False):
    print(f"Recovering block {index}")

    recovered = bytearray(BLOCK_SIZE)
    intermediate = bytearray(BLOCK_SIZE)

    prev_block = bytearray(blocks[index - 1])
    target_block = blocks[index]

    pad_len = 0

    if is_last:
        # Hardcoded since I got lazy and brute forced it myself lmao
        pad_len = 10

        for i in range(1, pad_len + 1):
            intermediate[-i] = pad_len ^ prev_block[-i]
            recovered[-i] = pad_len

    for byte_pos in reversed(range(BLOCK_SIZE - pad_len)):
        pad = BLOCK_SIZE - byte_pos

        for guess in range(256):
            modified_prev = prev_block.copy()

            for j in range(byte_pos + 1, BLOCK_SIZE):
                modified_prev[j] = intermediate[j] ^ pad

            modified_prev[byte_pos] = guess

            test_ct = (
                b"".join(blocks[:index - 1]) +
                bytes(modified_prev) +
                target_block
            )

            if oracle.query(test_ct):
                intermediate[byte_pos] = guess ^ pad
                recovered[byte_pos] = intermediate[byte_pos] ^ prev_block[byte_pos]

                byte = recovered[byte_pos]
                char = chr(byte) if 32 <= byte <= 126 else '.'
                print(f"Block {index} | Byte {byte_pos:2d} = {byte:02x} ('{char}')")
                break
        else:
            raise Exception(f"Failed recovering block {index} byte {byte_pos}")

    print(f"Finished block {index}: {recovered.decode(errors='ignore')}")
    return bytes(recovered)


def main():
    oracle = PaddingOracle()
    blocks = split_blocks(oracle.ciphertext)

    plaintext = b""

    for i in range(1, len(blocks)):
        is_last = (i == len(blocks) - 1)
        plaintext += recover_block(oracle, blocks, i, is_last=is_last)

    # Remove PKCS#7 padding
    pad = plaintext[-1]
    if 1 <= pad <= BLOCK_SIZE:
        plaintext = plaintext[:-pad]

    print("\nFINAL RECOVERED PLAINTEXT:")
    print(plaintext.decode(errors="ignore"))

    oracle.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
