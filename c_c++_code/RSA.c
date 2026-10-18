#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/err.h>

int main(void)
{
    int result = 1;

    EVP_PKEY_CTX *keygen_ctx = NULL;
    EVP_PKEY_CTX *encrypt_ctx = NULL;
    EVP_PKEY_CTX *decrypt_ctx = NULL;
    EVP_PKEY *key = NULL;

    unsigned char *ciphertext = NULL;
    unsigned char *decryptedtext = NULL;

    size_t ciphertext_len = 0;
    size_t decryptedtext_len = 0;

    const unsigned char plaintext[] = "test RSA";
    size_t plaintext_len = strlen((const char *)plaintext);

    // 1. RSA 키 쌍 생성
    keygen_ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
    if (keygen_ctx == NULL ||
        EVP_PKEY_keygen_init(keygen_ctx) <= 0 ||
        EVP_PKEY_CTX_set_rsa_keygen_bits(keygen_ctx, 2048) <= 0 ||
        EVP_PKEY_keygen(keygen_ctx, &key) <= 0) {
        fprintf(stderr, "RSA key generation failed.\n");
        goto cleanup;
    }

    printf("RSA-2048 key pair generated.\n");

    // 2. 공개키를 사용한 RSA-OAEP 암호화 설정
    encrypt_ctx = EVP_PKEY_CTX_new(key, NULL);
    if (encrypt_ctx == NULL ||
        EVP_PKEY_encrypt_init(encrypt_ctx) <= 0 ||
        EVP_PKEY_CTX_set_rsa_padding(
            encrypt_ctx, RSA_PKCS1_OAEP_PADDING) <= 0 ||
        EVP_PKEY_CTX_set_rsa_oaep_md(
            encrypt_ctx, EVP_sha256()) <= 0 ||
        EVP_PKEY_CTX_set_rsa_mgf1_md(
            encrypt_ctx, EVP_sha256()) <= 0) {
        fprintf(stderr, "Encryption initialization failed.\n");
        goto cleanup;
    }

    // 3. 암호문에 필요한 메모리 크기 확인
    if (EVP_PKEY_encrypt(
            encrypt_ctx, NULL, &ciphertext_len,
            plaintext, plaintext_len) <= 0) {
        fprintf(stderr, "Ciphertext size calculation failed.\n");
        goto cleanup;
    }

    ciphertext = OPENSSL_malloc(ciphertext_len);
    if (ciphertext == NULL) {
        fprintf(stderr, "Ciphertext memory allocation failed.\n");
        goto cleanup;
    }

    // 4. 공개키로 암호화
    if (EVP_PKEY_encrypt(
            encrypt_ctx, ciphertext, &ciphertext_len,
            plaintext, plaintext_len) <= 0) {
        fprintf(stderr, "Encryption failed.\n");
        goto cleanup;
    }

    printf("Ciphertext (%zu bytes): ", ciphertext_len);
    for (size_t i = 0; i < ciphertext_len; i++) {
        printf("%02x", ciphertext[i]);
    }
    printf("\n");

    // 5. 개인키를 사용한 복호화 설정
    decrypt_ctx = EVP_PKEY_CTX_new(key, NULL);
    if (decrypt_ctx == NULL ||
        EVP_PKEY_decrypt_init(decrypt_ctx) <= 0 ||
        EVP_PKEY_CTX_set_rsa_padding(
            decrypt_ctx, RSA_PKCS1_OAEP_PADDING) <= 0 ||
        EVP_PKEY_CTX_set_rsa_oaep_md(
            decrypt_ctx, EVP_sha256()) <= 0 ||
        EVP_PKEY_CTX_set_rsa_mgf1_md(
            decrypt_ctx, EVP_sha256()) <= 0) {
        fprintf(stderr, "Decryption initialization failed.\n");
        goto cleanup;
    }

    // 6. 복호화 결과에 필요한 메모리 크기 확인
    if (EVP_PKEY_decrypt(
            decrypt_ctx, NULL, &decryptedtext_len,
            ciphertext, ciphertext_len) <= 0) {
        fprintf(stderr, "Decrypted text size calculation failed.\n");
        goto cleanup;
    }

    decryptedtext = OPENSSL_malloc(decryptedtext_len + 1);
    if (decryptedtext == NULL) {
        fprintf(stderr, "Decryption memory allocation failed.\n");
        goto cleanup;
    }

    // 7. 개인키로 복호화
    if (EVP_PKEY_decrypt(
            decrypt_ctx, decryptedtext, &decryptedtext_len,
            ciphertext, ciphertext_len) <= 0) {
        fprintf(stderr, "Decryption failed.\n");
        goto cleanup;
    }

    // 8. 문자열 출력용 종료 문자 추가
    decryptedtext[decryptedtext_len] = '\0';

    printf("Decrypted text: %s\n", decryptedtext);

    if (decryptedtext_len != plaintext_len ||
        memcmp(decryptedtext, plaintext, plaintext_len) != 0) {
        fprintf(stderr, "Verification failed.\n");
        goto cleanup;
    }

    printf("Encryption/decryption test: PASS\n");
    result = 0;

cleanup:
    if (result != 0) {
        ERR_print_errors_fp(stderr);
    }

    OPENSSL_free(ciphertext);
    OPENSSL_free(decryptedtext);

    EVP_PKEY_CTX_free(keygen_ctx);
    EVP_PKEY_CTX_free(encrypt_ctx);
    EVP_PKEY_CTX_free(decrypt_ctx);
    EVP_PKEY_free(key);

    return result;
}
