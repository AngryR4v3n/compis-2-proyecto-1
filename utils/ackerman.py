def A(m, n):
    print(m, n)
    if m == 0:
        return n + 1
    if n == 0:
        return A(m - 1, 1)
    n2 = A(m, n - 1)
    return A(m - 1, n2)
 
print(A(2, 1))