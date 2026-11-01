import time
import random
import statistics
import csv

# --------------------------------
# 1. 취약한 RSA 모듈러 거듭제곱
# --------------------------------

def vulnerable_mod_exp(base, exponent, modulus):
    result = 1
    base %= modulus

    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus

        base = (base * base) % modulus
        exponent >>= 1

    return result


# --------------------------------
# 2. Hamming Weight 계산
# --------------------------------

def hamming_weight(number):
    return bin(number).count("1")


# --------------------------------
# 3. 실행 시간 측정
# --------------------------------

def measure_time(base, exponent, modulus, repeat=1000):

    times = []

    # 워밍업
    for _ in range(100):
        vulnerable_mod_exp(base, exponent, modulus)

    for _ in range(repeat):
        start = time.perf_counter_ns()

        vulnerable_mod_exp(base, exponent, modulus)

        end = time.perf_counter_ns()

        times.append(end - start)

    return times


# --------------------------------
# 4. 실험용 비밀 지수 생성
# --------------------------------

def generate_exponents():

    bit_length = 16

    exponents = []

    for weight in range(2, bit_length):
        candidates = [
            x for x in range(1 << (bit_length - 1), 1 << bit_length)
            if hamming_weight(x) == weight
        ]

        exponents.append(random.choice(candidates))

    return exponents


# --------------------------------
# 5. 타이밍 공격 실험
# --------------------------------

def run_experiment():

    modulus = (1 << 2048) - 159
    base = 123456789

    exponents = generate_exponents()

    results = []

    for exponent in exponents:

        times = measure_time(
            base,
            exponent,
            modulus,
            repeat=1000
        )

        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        std_time = statistics.stdev(times)

        weight = hamming_weight(exponent)

        results.append({
            "exponent": exponent,
            "hamming_weight": weight,
            "average_ns": avg_time,
            "median_ns": median_time,
            "std_ns": std_time
        })

        print(
            f"HW={weight:2d} | "
            f"Average={avg_time:.2f} ns | "
            f"Median={median_time:.2f} ns"
        )

    return results


# --------------------------------
# 6. CSV 저장
# --------------------------------

def save_results(results):

    with open(
        "timing_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "exponent",
                "hamming_weight",
                "average_ns",
                "median_ns",
                "std_ns"
            ]
        )

        writer.writeheader()
        writer.writerows(results)


# --------------------------------
# 7. 실행
# --------------------------------

if __name__ == "__main__":

    results = run_experiment()

    save_results(results)

    print("\n실험 완료")
    print("결과 파일: 포폴용 개발작\\부채널 공격\\timing_results.csv")