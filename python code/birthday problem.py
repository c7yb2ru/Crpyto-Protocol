import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

def birthday_problem(n, trials, days=365):
    """n명 중 생일이 겹치는 사람이 있을 확률을 시뮬레이션으로 추정"""
    shared = 0
    for _ in range(trials):
        birthdays = [random.randint(1, days) for _ in range(n)]
        if len(birthdays) != len(set(birthdays)):
            shared += 1
    return shared / trials

def exact_prob(n, days=365):
    """이론값: 1 - prod((days - i) / days)"""
    p_no_collision = 1.0
    for i in range(n):
        p_no_collision *= (days - i) / days
    return 1 - p_no_collision

'''
def plot_birthday_problem(max_people, trials):
    people_counts = list(range(1, max_people + 1))
    probabilities = [birthday_problem(n, trials) for n in people_counts]
    exact = [exact_prob(n) for n in people_counts]   # 함수 안으로 이동

    df = pd.DataFrame({'Number of People': people_counts,
                       'Probability': probabilities})

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Number of People', y='Probability',
                 marker='o', label='Simulation')
    plt.plot(people_counts, exact, color='green', label='Exact')  # 함수 안으로 이동
    plt.axhline(0.5, color='red', linestyle='--', label='50% Probability')
    plt.title('Birthday Problem: Simulation vs Exact')
    plt.xlabel('Number of People in the Group')
    plt.ylabel('Probability of Shared Birthday')
    plt.legend()
    plt.grid()
    plt.show()
'''
def first_n_over_half(days):
    n = 1
    while exact_prob(n, days) < 0.5:
        n += 1
    return n

for days in [365, 1000, 10000, 100000, 1000000]:
    n = first_n_over_half(days)
    print(f"days={days:>8}  n={n:>5}  n/sqrt(days)={n / math.sqrt(days):.3f}")
