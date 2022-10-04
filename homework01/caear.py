def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for i in range(len(plaintext)):
        char = plaintext[i]
        if ord(char) >= 65 and ord(char) <= 90:
            char = chr(ord(char) + shift)
            if ord(char) > 90:
                char = chr(ord(char) - 26)
        elif ord(char) >= 97 and ord(char) <= 122:
            char = chr(ord(char) + shift)
            if ord(char) > 122:
                char = chr(ord(char) - 26)
        ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if ord(char) >= 65 and ord(char) <= 90:
            char = chr(ord(char) - shift)
            if ord(char) < 65:
                char = chr(ord(char) + 26)
        elif ord(char) >= 97 and ord(char) <= 122:
            char = chr(ord(char) - shift)
            if ord(char) < 97:
                char = chr(ord(char) + 26)
        plaintext += char

    return plaintext
