import random, os, time
import numpy as np
import encryption
from PIL import Image
from Crypto.Util.strxor import strxor

# Secret
p = 10 #random.randint(2,250)
q = 20 #random.randint(2,250)
m = 5
r = 2.2 + random.random()*0.1

def encryption_oracle(plain_image):
    init = random.random()
    return encryption.encrypt(plain_image, p, q, m, init, r)

def weak_logistic_map():

    # Repeated static keystream
    init = random.random()
    r = 2.2 + random.random()*0.1
    keystream = encryption.logistic_map(init, r, 1000)
    print("keystream:", keystream)

    # Repeated periodic keystream
    init = random.random()
    r = 3.4 + random.random()*0.1
    keystream = encryption.logistic_map(init, r, 1000)
    print("keystream:", keystream)

def recover_pq(size):
    payload = Image.new("RGB", (size, size))
    payload.putpixel((1,0), (255,255,255))

    response = encryption_oracle(payload)

    cipher_img = response.load()

    permuted = []
    for x in range(size):
        for y in range(size):
            lsb = cipher_img[x,y][0] & 0xF
            if lsb == 255 & 0xF:
                permuted.append((x,y))
        
        if len(permuted) == 1:
            break

    print("x1: ", permuted[0][0])
    print("y1: ", permuted[0][1])
    print("\n[*] Recover p and q by running recover_pq.sage script")