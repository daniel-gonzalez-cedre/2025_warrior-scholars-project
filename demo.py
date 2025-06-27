import random
from math import ceil, sqrt

def str_to_int(s: str) -> int:
  return int.from_bytes(s.encode(), byteorder="little")

def int_to_str(i: int) -> str:
  length = ceil(i.bit_length() / 8)
  return i.to_bytes(length, byteorder="little").decode()

# check to see whether or not this number is composite
# by attempting to find a non-trivial divisor
def is_prime(x):
  for n in range(2, int(sqrt(x) + 1)):
    if x % n == 0:
      return False
  return True

# find the gcd of x and y
# using the Euclidean division algorithm
def gcd(x, y):
  x, y = (max(x, y), min(x, y))
  q = 1
  while x >= y * q:
    q += 1
  q -= 1
  r = x - y*q

  if r == 0:
    return y
  else:
    return gcd(y, r)

def compute_moduli(p, q):
  n = p*q  # public modulus
  phi = (p - 1)*(q - 1)  # private modulus
  return (n, phi)

def choose_private_key(phi):
  while True:
    d, = random.sample(range(2, phi), 1)
    if gcd(d, phi) == 1:
      break
  return d

# finds the multiplicative inverse of d modulo phi
# using the Extended Euclidean division algorithm
def mult_inverse(d, phi, s=None, t=None):
  assert gcd(d, phi) == 1, f'{d} and {phi} are not relatively prime!'
  s = [1, 0] if s is None else s
  t = [0, 1] if t is None else t

  d, phi = (min(d, phi), max(d, phi))

  q = 1
  while phi >= d * q:
    q += 1
  q -= 1
  r = phi - d*q

  if r == 0:
    return t[-1]
  else:
    s += [s[-2] - q*s[-1]]
    t += [t[-2] - q*t[-1]]
    return mult_inverse(r, d, s=s, t=t)

# efficiently computes x ≡ aᵇ (mod m)
def modular_exp(a, b, m):
  result = 1
  for k in range(b):
    result = result*a % m
  return result

if __name__ == "__main__":
  message = input("> message (default = 435): ")

  print(f"Your message is: {message}")

  bytecode = str_to_int(message)
  print(f"After conversion to bytes: {bytecode}")

  # M = 435 if not message else int(message)
  M = bytecode
  print(f"The bytecode that needs to be transmitted is:\nM = {M}")
  # print(f"M = {M} is the message that needs to be transmitted.")

  #p = 79
  #q = 101
  print()
  p = int(input("> define p: "))
  if is_prime(p):
    print(f"\tp = {p} is prime.")
  else:
    raise Exception(f"{p} is NOT prime. Pick a different value.")

  print()
  q = int(input("> define q: "))
  if is_prime(q):
    print(f"\tq = {q} is prime.")
  else:
    raise Exception(f"{q} is NOT prime. Pick a different value.")

  # public and private moduli, respectively
  n, phi = compute_moduli(p, q)

  print(f"\tn = {n} is our public modulus.")
  print(f"\tφ(n) = {phi} is our private modulus.")

  print()
  d_optional = input("> define d (optional): ")

  # private key
  d = choose_private_key(phi) if d_optional == "" else int(d_optional)
  # public key
  e = mult_inverse(d, phi) % phi

  print()
  print(f"d = {d} is our private key -- used for decryption.")
  print(f"e = {e} is our public key -- used for encryption.")
  print()

  # encrypting the message
  c = modular_exp(M, e, n)
  print(f"c = {c} is our encrypted cypher text.")

  # decrypting the message
  message = modular_exp(c, d, n)
  print(f"Our decrypted message is {message}.")
