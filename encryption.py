import random, os
import hashlib
import numpy as np
import time
from sympy import Matrix
from PIL import Image

def ACM(img, p, q, m):

    counter = 0
    
    if img.mode == "P":
        img = img.convert("RGB")

    assert img.size[0] == img.size[1]

    while counter < m:
        dim = width, height = img.size

        with Image.new(img.mode, dim) as canvas:
            for x in range(width):
                for y in range(height):
                    nx = (x + y*p) % width
                    ny = (x*q + y*(p*q + 1)) % height

                    canvas.putpixel((nx, ny), img.getpixel((x, y)))

        img = canvas
        counter += 1

    return canvas

def inv_ACM(img, p, q, m):
    counter = 0
    if img.mode == "P":
        img = img.convert("RGB")

    assert img.size[0] == img.size[1]
    
    matrix = Matrix(np.array([[1, p], [q, p*q + 1]]))
    inv_matrix = matrix.inv_mod(img.size[0])
    while counter < m:
        dim = width, height = img.size

        with Image.new(img.mode, dim) as canvas:
            for x in range(width):
                for y in range(height):
                    nx = (x*inv_matrix[0] + y*inv_matrix[1]) % width
                    ny = (x*inv_matrix[2] + y*inv_matrix[3]) % height

                    canvas.putpixel((nx, ny), img.getpixel((x, y)))

        img = canvas
        counter += 1

    return canvas

def logistic_map(init, r, length, prec=4):

    x = [None] * (length+1)
    x[0] = init
    for i in range(1,length+1):
        x[i] = r * x[i-1] * (1 - x[i-1])

    keystream = [None] * length
    for i in range(length):
        if x[i] < 0:
            keystream[i] = 0
        else:
            try:
                float_point = int(str(x[i]).split(".")[1][:prec].replace("e","").replace("-",""))
                keystream[i] = float_point & 0xF # 4 LSB bits
            except IndexError:
                keystream[i] = 0

    return keystream

def selective_xor(m, k):
    c = []
    for i in range(len(m)):
        bit_len = int(m[i]).bit_length()
        if bit_len > 4:
            msb = m[i] >> 4 & (2**(bit_len-4) - 1)
        else:
            msb = 0
        # 4 bit MSB ^ 4 bit key + 4 bit LSB
        xored = ((msb ^ k[i % len(k)]) << 4) | (m[i] & 0xF)
        c.append(xored)

    return bytes(c)

def encrypt(plain_image, p, q, m, init, r):

    cipher_image = ACM(plain_image, p, q, m)
    
    keystream = logistic_map(init, r, cipher_image.size[0]**2)
    image_byte = np.array(cipher_image).flatten()
    encrypted_byte = selective_xor(image_byte, keystream)
    return Image.frombytes(cipher_image.mode, cipher_image.size, encrypted_byte)

def decrypt(cipher_image, p, q, m, init, r):

    keystream = logistic_map(init, r, cipher_image.size[0]**2)
    image_byte = np.array(cipher_image).flatten()
    
    decrypted_byte = selective_xor(image_byte, keystream)
    plain_image = Image.frombytes(cipher_image.mode, cipher_image.size, decrypted_byte)
    plain_image = inv_ACM(plain_image, p, q, m)

    return plain_image