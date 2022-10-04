def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    if len(plaintext) > len(keyword):
        x = len(plaintext) // len(keyword)
        keyword *= x + 2
    for i in range(len(plaintext)):
        shift = ord(keyword[i])
        char = plaintext[i]
        if shift >= 65 and shift <= 90:
            shift -= 65
        elif shift >= 97 and shift <= 122:
            shift -= 97
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


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    if len(ciphertext) > len(keyword):
        x = len(ciphertext) // len(keyword)
        keyword *= x + 2
    for i in range(len(ciphertext)):
        shift = ord(keyword[i])
        char = ciphertext[i]
        if shift >= 65 and shift <= 90:
            shift -= 65
        elif shift >= 97 and shift <= 122:
            shift -= 97
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
