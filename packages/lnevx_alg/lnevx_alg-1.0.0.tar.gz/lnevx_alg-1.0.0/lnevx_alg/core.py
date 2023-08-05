# -*- coding: utf-8 -*-


def encrypt(message, password):
    length = len(password)
    if length > 31:
        return 'Error! Password must be less, then 31 characters'

    # Жесткое кодирование
    crypt_message = []

    for word in message:
        code = ord(word)
        code -= length
        crypt_message.append(chr(code))

    crypt_message = ''.join(crypt_message)

    # Тонкое кодирование
    shift = 10
    chrs = list(password)
    crypt_chrs = []
    i = 0

    for character in chrs:
        crypt_chrs.append(chr(ord(character) - shift))
        i += 1

    crypt_message2 = list(crypt_message)

    for character in crypt_chrs:
        i = 0
        amount = len(crypt_message2) // shift
        for j in range(1, amount + 1):
            crypt_message2.insert(shift * j + i, character)
            i += 1

    crypt_message = ''.join(crypt_message2)

    return crypt_message
