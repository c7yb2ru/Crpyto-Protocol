from Crypto.Cipher import AES
import os

class AESCipher:
    def __init__(self, key, iv): # aes 암호 생성자, key와 iv를 받아서 초기화
        self.key = key
        self.iv = iv
        self.cipher = AES.new(key, AES.MODE_CBC, iv) # AES 객체 생성, CBC 모드로 초기화

    def encrypt(self, plaintext):
        # PKCS7 padding 적용, AES 블록 크기는 16바이트이므로, plaintext의 길이를 16의 배수로 만들어야 함
        padding_length = 16 - (len(plaintext) % 16)
        plaintext += bytes([padding_length] * padding_length)

        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext): # AES 암호 해독 함수, ciphertext를 받아서 복호화된 plaintext를 반환
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = cipher.decrypt(ciphertext)

        padding_length = plaintext[-1]
        return plaintext[:-padding_length]


key = os.urandom(16)
iv = os.urandom(16)

aes = AESCipher(key, iv)

print("Input message:")
msg = input().encode()

ciphertext = aes.encrypt(msg)
print("Ciphertext:", ciphertext.hex())

plaintext = aes.decrypt(ciphertext)
print("Decrypted:", plaintext.decode())
