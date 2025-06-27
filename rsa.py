from math import ceil, gcd
from random import randint

def str_to_int(s: str) -> int:
  return int.from_bytes(s.encode(), byteorder="little")

def int_to_str(i: int) -> str:
  length = ceil(i.bit_length() / 8)
  return i.to_bytes(length, byteorder="little").decode()

# 2055974649969437862219
M = "Kill Cato"

p = 97
q = 269
n = p*q
phi = (p - 1)*(q - 1)
while True:
  d = randint(2, phi)
  if gcd(d, phi) == 1:
    break

for candidate in range(2, phi):
  if (candidate*d) % phi == 1:
    e = candidate
    break

original = []
encrypted = []
for char in M:
  integer = str_to_int(char)
  original.append(integer)

  c = (integer**e) % n
  encrypted.append(c)

decrypted = []
message = ""
for cipher in encrypted:
  m = (cipher**d) % n
  decrypted.append(m)
  message = message + int_to_str(m)

print(M)
print(original)
print(encrypted)
print(decrypted)
print(message)
