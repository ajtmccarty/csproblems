from secrets import token_bytes
import sys
from typing import Tuple


def random_key(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")


def encrypt(message: str) -> Tuple[int, int]:
    message_bytes: bytes = message.encode()
    key: int = random_key(len(message_bytes))
    message_int: int = int.from_bytes(message_bytes, "big")
    cipher_int: int = message_int ^ key
    return [cipher_int, key]


def decrypt(message_int: int, key: int) -> str:
    plaintext_int: int = message_int ^ key
    plaintext_bytes: bytes = plaintext_int.to_bytes(
        (plaintext_int.bit_length() + 7) // 8, "big"
    )
    return plaintext_bytes.decode()


if __name__ == "__main__":
    msg: str = " ".join(sys.argv[1:])
    print(f"Plaintext: {msg}")
    cipher_text, key = encrypt(msg)
    print(f"Ciphertext: {cipher_text}")
    print(f"Key:        {key}")
    decrypted = decrypt(cipher_text, key)
    print(f"Decrypted: {decrypted}")
