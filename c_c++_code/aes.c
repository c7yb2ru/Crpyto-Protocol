
#include <stdio.h>
#include <string.h>
#include <openssl/aes.h>

int main(void) {
    // AES-128 key and initialization vector: 16 bytes each
    const char *key_string = "0123456789ABCDEF";
    const char *iv_string = "ABCDEF9876543210";
    unsigned char iv[AES_BLOCK_SIZE];
    memcpy(iv, iv_string, AES_BLOCK_SIZE);
    // Input plaintext
    unsigned char plaintext[] = "Hello, World!";
    size_t plaintext_len = sizeof(plaintext) - 1;

    // PKCS#7 padding to a multiple of AES block size (16 bytes)
    size_t padded_len = ((plaintext_len / AES_BLOCK_SIZE) + 1)
                        * AES_BLOCK_SIZE;
    unsigned char padded_plaintext[128] = {0};
    unsigned char ciphertext[128] = {0};
    unsigned char decryptedtext[128] = {0};

    memcpy(padded_plaintext, plaintext, plaintext_len);
    unsigned char pad = (unsigned char)(padded_len - plaintext_len);
    memset(padded_plaintext + plaintext_len, pad, pad);

    // AES encryption
    AES_KEY enc_key;
    if (AES_set_encrypt_key((const unsigned char *)key_string, 128, &enc_key) != 0) {
        fprintf(stderr, "Failed to set encryption key\n");
        return 1;
    }

    AES_cbc_encrypt(
        padded_plaintext, ciphertext, padded_len,
        &enc_key, iv, AES_ENCRYPT
    );

    printf("Ciphertext: ");
    for (size_t i = 0; i < padded_len; i++) {
        printf("%02x", ciphertext[i]);
    }
    printf("\n");

    // Reset IV to the original value for decryption
    memcpy(iv, iv_string, AES_BLOCK_SIZE);

    // AES decryption
    AES_KEY dec_key;
    if (AES_set_decrypt_key((const unsigned char *)key_string, 128, &dec_key) != 0) {
        fprintf(stderr, "Failed to set decryption key\n");
        return 1;
    }

    AES_cbc_encrypt(
        ciphertext, decryptedtext, padded_len,
        &dec_key, iv, AES_DECRYPT
    );

    // Validate and remove PKCS#7 padding
    unsigned char pad_len = decryptedtext[padded_len - 1];
    if (pad_len == 0 || pad_len > AES_BLOCK_SIZE ||
        pad_len > padded_len) {
        fprintf(stderr, "Invalid padding\n");
        return 1;
    }

    for (size_t i = padded_len - pad_len; i < padded_len; i++) {
        if (decryptedtext[i] != pad_len) {
            fprintf(stderr, "Invalid padding\n");
            return 1;
        }
    }

    decryptedtext[padded_len - pad_len] = '\0';
    printf("Decrypted text: %s\n", decryptedtext);

    return 0;
}

