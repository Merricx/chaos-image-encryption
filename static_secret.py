import random, os, time
import numpy as np
import encryption
from PIL import Image
from Crypto.Util.strxor import strxor
from sympy import *
from sympy.solvers.solveset import linsolve


# Secret
p = random.randint(2,250)
q = random.randint(2,250)
m = random.randint(2,10)
init = random.random()
r = 3 + random.random()


def encryption_oracle(plain_image):

    return encryption.encrypt(plain_image, p, q, m, init, r)

def recover_keystream(size):

    # Generate full-black image
    plain_image = Image.new("RGB", (size, size))

    # Send image to encryption oracle
    cipher_image = encryption_oracle(plain_image)

    # Convert plain_image and cipher_image to bytes
    plain_image_bytes = bytes(np.array(plain_image).flatten().tolist())
    cipher_image_bytes = bytes(np.array(cipher_image).flatten().tolist())

    # Recover 8-bit keystream
    k = list(strxor(plain_image_bytes, cipher_image_bytes))

    # Get 4-bit MSB keystream
    keystream = []
    for i in range(size**2):
        bit_len = int(k[i]).bit_length()
        if bit_len > 4:
            msb = k[i] >> 4 & (2**(bit_len-4) - 1)
        else:
            msb = 0
        
        keystream.append(msb)
    

    return keystream

def recover_m():

    one_exec_time = 12 # avg. time of one encryption execution (depends on the machine)

    start_time = time.time()
    payload = Image.new("RGB", (1024, 1024))

    encryption_oracle(payload)

    end_time = time.time()
    elapsed_time = end_time - start_time
    m = int(elapsed_time // one_exec_time)

    possible_m = [m, m-1, m+1]

    return possible_m

def recover_pq(keystream, size):

    payload = Image.new("RGB", (size, size))
    payload.putpixel((1,0), (255,255,255))

    response = encryption_oracle(payload)

    response_bytes = np.array(response).flatten()

    decrypted_response = encryption.selective_xor(response_bytes, keystream)

    permuted_img = Image.frombytes("RGB", (size,size), decrypted_response).load()

    permuted = []
    for x in range(size):
        for y in range(size):
            if permuted_img[x,y] == (255,255,255):
                permuted.append((x,y))
        
        if len(permuted) == 1:
            break

    print("x1: ", permuted[0][0])
    print("y1: ", permuted[0][1])
    print("\n[*] Recover p and q by running recover_pq.sage script")

if __name__ == "__main__":
    
    print("[*] Generated static keys:")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"m = {m}")
    print(f"r = {r}")
    print(f"x0 = {init}\n")

    print("[+] Recover keystream...")
    keystream = recover_keystream(512)
    
    real_keystream = encryption.logistic_map(init, r, 512**2)
    assert keystream == real_keystream

    print("[+] Recover m with Timing Attack...")
    possible_m = recover_m()
    print("[+] Possible m:", possible_m)

    print("[+] Recover permutation position...")
    recover_pq(keystream, 512)
    