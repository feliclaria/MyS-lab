from time import time
from random import random
from collections import Counter
import discrete as disc
import numpy as np
import simulate as sim
import math

iters = [100, 1_000, 10_000, 100_000]


def ex1_shuffle_cards(N=100):
  stack = list(range(N))
  shuffled = []

  for i in range(N):
    card = stack[disc.randint(N-i) - 1]
    stack.remove(card)
    shuffled.append(card)

  return shuffled

def ex1_random_var(N=100):
  cards = ex1_shuffle_cards(N)
  return sum(cards[i] == i for i in range(N))

def ex1_is_success_i(cards, r=10):
  i = 0
  is_success = True

  while is_success and i < r:
    is_success = is_success and cards[i] == i
    i += 1

  return is_success

def ex1_is_success_ii(cards, r=10):
  i = 0
  is_success = True

  while is_success and i < r:
    is_success = is_success and cards[i] == i
    i += 1

  while is_success and i < len(cards):
    is_success = is_success and cards[i] != i
    i += 1

  return is_success

def ex1():
  results_1a_i = [sim.success_prob(n, ex1_shuffle_cards, ex1_is_success_i) for n in iters]
  results_1a_ii = [sim.success_prob(n, ex1_shuffle_cards, ex1_is_success_ii) for n in iters]
  expected_vals = [sim.expected_value(n, ex1_random_var) for n in iters]
  variances = [sim.variance(iters[i], ex1_random_var, expected_vals[i]) for i in range(len(iters))]

  print(f'Iteraciones: \t{iters}')
  print(f'Ej. 1a.i: \t{results_1a_i}')
  print(f'Ej. 1a.ii: \t{results_1a_ii}')
  print(f'Esperanza: \t{expected_vals}')
  print(f'Varianza: \t{variances}')


def ex2():
  n = 100
  N = 10_000
  f = lambda k: np.exp(k/N)

  start = time()
  monte_carlo = sim.monte_carlo_disc(n, N, f)
  print(f'Aprox. con {n} v. a.: \t{monte_carlo} \t({time() - start}s)')

  start = time()
  partial_sum = sum(f(k+1) for k in range(n))
  print(f'Primeros {n} términos: \t{partial_sum} \t({time() - start}s)')

  start = time()
  total_sum = sum(f(k+1) for k in range(N))
  print(f'Suma exacta: \t\t{total_sum} \t({time() - start}s)')


def ex3_random_var():
  seen = []
  N = 0

  while len(seen) < 11:
    N += 1
    X = disc.randint(6) + disc.randint(6)
    if X not in seen:
      seen.append(X)

  return N

def ex3():
  expected_vals = [sim.expected_value(n, ex3_random_var) for n in iters]
  std_deviations = [sim.std_deviation(iters[i], ex3_random_var, expected_vals[i]) for i in range(len(iters))]
  is_success_i = [sim.success_prob(n, ex3_random_var, lambda N: N >= 15) for n in iters]
  is_success_ii = [sim.success_prob(n, ex3_random_var, lambda N: N <= 9) for n in iters]

  print(f'Iteraciones: \t\t{iters}')
  print(f'Esperanza: \t\t{expected_vals}')
  print(f'Desviación estándar: \t{std_deviations}')
  print(f'Prob. N >= 15: \t\t{is_success_i}')
  print(f'Prob. N <= 9: \t\t{is_success_ii}')


def ex4():
  probs_X = [0.11, 0.14, 0.09, 0.08, 0.12, 0.10, 0.09, 0.07, 0.11, 0.09]
  values_X = list(i for i in range(1,11))

  Y = lambda: disc.randint(10) - 1
  probs_Y = [1/10 for _ in range(10)]

  """
  p_j / q_j <= c
  => p_j / (1/10) <= c
  => 10 * p_j <= c
  => 0.12 <= p_j <= c / 10
  => 0.12 * 10 <= c
  => 1.2 <= c
  """
  c = 1.2
  n = 10_000

  start = time()
  [disc.accept_reject(Y, probs_X, probs_Y, c) for _ in range(n)]
  print(f'Método de aceptación y rechazo: \t{time() - start}s')

  start = time()
  [disc.inverse_trans_arr(probs_X, values_X) for _ in range(n)]
  print(f'Método de transformada inversa: \t{time() - start}s')

  start = time()
  [disc.urn_random(probs_X, values_X) for _ in range(n)]
  print(f'Método de la urna: \t\t\t{time() - start}s')


def ex5_binomial(n, p):
  return sum(random() <= p for _ in range(n))

def ex5():
  sims = 10_000
  n = 10
  p = 0.3

  start = time()
  results_i = [disc.binomial(n, p) for _ in range(sims)]
  end = time()
  ocurrences_i = Counter(results_i)

  print(f'Bin({n}, {p}) con transformada inversa')
  print(f'  Tiempo: \t\t{end - start}s')
  print(f'  Mayor ocurrencia: \t{ocurrences_i.most_common(1)[0][0]}')
  print(f'  P[X = 0]: \t\t{ocurrences_i[0] / sims}')
  print(f'  P[X = 10]: \t\t{ocurrences_i[10] / sims}\n')

  start = time()
  results_ii = [ex5_binomial(n, p) for _ in range(sims)]
  end = time()
  ocurrences_ii = Counter(results_ii)

  print(f'Bin({n}, {p}) con simulación naive')
  print(f'  Tiempo: \t\t{end - start}s')
  print(f'  Mayor ocurrencia: \t{ocurrences_ii.most_common(1)[0][0]}')
  print(f'  P[X = 0]: \t\t{ocurrences_ii[0] / sims}')
  print(f'  P[X = 10]: \t\t{ocurrences_ii[10] / sims}\n')

  print(f'Bin({n}, {p}) teórica')
  print(f'  Mayor ocurrencia: \t{int((n+1)*p)}')
  print(f'  P[X = 0]: \t\t{math.comb(n, 0) * (1-p)**(n)}')
  print(f'  P[X = 10]: \t\t{math.comb(n, 10) * p**10 * (1-p)**(n-10)}')


def ex6_inverse_trans_optimized():
  U = random()
  if U < 0.35: return 3
  elif U < 0.55: return 1
  elif U < 0.75: return 4
  elif U < 0.90: return 0
  else: return 2

def ex6_inverse_trans():
  U = random()
  if U < 0.15: return 0
  elif U < 0.35: return 1
  elif U < 0.45: return 2
  elif U < 0.80: return 3
  else: return 4

def ex6():
  sims = 10_000

  start = time()
  [ex6_inverse_trans_optimized() for _ in range(sims)]
  end = time()
  print(f'Trans. inversa (ordenada): \t\t{end - start}s')

  start = time()
  [ex6_inverse_trans() for _ in range(sims)]
  end = time()
  print(f'Trans. inversa (desordenada): \t\t{end - start}s')

  start = time()
  [disc.inverse_trans_arr([0.35, 0.20, 0.20, 0.15, 0.10], [3, 1, 4, 0, 2]) for _ in range(sims)]
  end = time()
  print(f'Trans. inversa cíclica (ordenada): \t{end - start}s')

  start = time()
  [disc.inverse_trans_arr([0.15, 0.20, 0.10, 0.35, 0.20], [0, 1, 2, 3, 4]) for _ in range(sims)]
  end = time()
  print(f'Trans. inversa cíclica (desordenada): \t{end - start}s')

  n = 4
  p = 0.45

  Y = lambda: disc.binomial(n, p)
  probs_Y = [math.comb(n, k) * p**k * (1-p)**(4-k) for k in range(n+1)]
  probs_X = [0.15, 0.20, 0.10, 0.35, 0.20]
  c = max(probs_X[i] / probs_Y[i] for i in range(n+1))

  start = time()
  [disc.accept_reject(Y, probs_X, probs_Y, c) for _ in range(sims)]
  end = time()
  print(f'Aceptación y rechazo: \t\t{end - start}s')


def ex7():
  n = 1_000
  lambd = 0.7

  is_success = lambda Y: Y > 2
  prob = sim.success_prob(n, lambda: disc.poisson(lambd), is_success)
  prob_optimized = sim.success_prob(n, lambda: disc.poisson_fast(lambd), is_success)

  print(f'P[Y > 2] con transformada inversa: \t\t{prob}')
  print(f'P[Y > 2] con transformada inversa mejorada: \t{prob_optimized}')


def ex8_X_pmf(i, k, lambd):
  g = lambda x: lambd**x / math.factorial(x) * math.exp(-lambd)
  return g(i) / sum(g(j) for j in range(k+1))

def ex8_X_inverse_trans(k, lambd):
  values = list(range(k+1))
  probs = [ex8_X_pmf(i, k, lambd) for i in values]
  return lambda: disc.inverse_trans_arr(probs, values)

def ex8_X_accept_reject(k, lambd):
  values_X = range(k+1)
  probs_X = [ex8_X_pmf(i, k, lambd) for i in values_X]

  Y = lambda: disc.randint(k+1)-1
  values_Y = range(k+1)
  probs_Y = [1/(k+1) for _ in values_Y]

  c = max(probs_X[i] / probs_Y[i] for i in range(len(probs_X)))

  return lambda: disc.accept_reject(Y, probs_X, probs_Y, c)

def ex8b():
  k = 10
  lambd = 0.7

  X_inverse_trans = ex8_X_inverse_trans(k, lambd)
  X_accept_reject = ex8_X_accept_reject(k, lambd)

  n = 1_000
  is_success = lambda X: X > 2

  result = 1 - sum(ex8_X_pmf(i, k, lambd) for i in range(3))
  result_inverse_trans = sim.success_prob(n, X_inverse_trans, is_success)
  result_accept_reject = sim.success_prob(n, X_accept_reject, is_success)

  print(f'P[X > 2] = {result}')
  print(f'Transformada inversa: \t{result_inverse_trans}')
  print(f'Aceptacón y rechazo: \t{result_accept_reject}')

def ex8_Xab_pmf(i, a, b, lambd):
  if i < a or i > b:
    return 0
  g = lambda x: lambd**x / math.factorial(x) * math.exp(-lambd)
  return g(i) / sum(g(j) for j in range(a, b+1))

def ex8_Xab_accept_reject(a, b, lambd):
  Y = lambda: disc.randint(b+1)-1

  pmf_X = lambda i: ex8_Xab_pmf(i, a, b, lambd)
  pmf_Y = lambda _: 1/(b+1)

  values_X = range(a, b+1)
  values_Y = range(b+1)

  probs_X = [pmf_X(i) for i in values_Y]
  probs_Y = [pmf_Y(i) for i in values_Y]

  c = max(pmf_X(i) / pmf_Y(i) for i in values_X)

  return lambda: disc.accept_reject(Y, probs_X, probs_Y, c)

def ex8c():
  a = 0
  b = 10
  lambd = 0.7

  Xab_accept_reject = ex8_Xab_accept_reject(a, b, lambd)

  n = 1_000
  is_success = lambda X: X > 2

  result = 1 - sum(ex8_Xab_pmf(i, a, b, lambd) for i in range(3))
  result_accept_reject = sim.success_prob(n, Xab_accept_reject, is_success)

  print(f'P[X > 2] = {result}')
  print(f'Aceptacón y rechazo: \t{result_accept_reject}')

def ex8():
  # ex8b()
  ex8c()


def ex9():
  return None


def main():
  ex8()

if __name__ == '__main__':
  main()
