#!/usr/bin/env sage
def recover_pq(m, x0, y0, x1, y1, N):

    var('p,q')
    xy = matrix(2,1,[x0,y0])
    A = matrix([[1,p],[q, p*q + 1]])

    pos_result = solve_mod([
        (A^m * xy)[0][0] == x1,
        (A^m * xy)[1][0] == y1
        ], N)

    return pos_result

if __name__ == "__main__":

    m = 7 # ACM iteration
    x0 = 1
    y0 = 0
    N = 512 # image size

    x1 = int(raw_input("x1: "))
    y1 = int(raw_input("y1: "))
    m = int(raw_input("m: "))

    print("Possible p,q: ")
    print(recover_pq(m, x0, y0, x1, y1, N))