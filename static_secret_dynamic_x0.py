import random, os, time
import numpy as np
import encryption
from PIL import Image
from Crypto.Util.strxor import strxor

# Secret
p = 10#random.randint(2,250)
q = 20#random.randint(2,250)
m = 5
init = 0.578#random.random()
r = 3 + 0.4764#random.random()

def encryption_oracle(plain_image):

    return encryption.encrypt(plain_image, p, q, m, init, r)

def logistic_map_analysis():
    init = 0.8927173285063715
    r = 3.5157732279084075
    print('x0:', init)
    print('r :', r)
    print('keystream:', encryption.logistic_map(init, r, 100, 10))
    print()

logistic_map_analysis()