def d(x, y):
    if x % y == 0:
        return True
    return False


for A in range(100, 0, -1):
    flag = True
    for x in range(1, 100):
        for y in range(1, 100):
            if not ((not d(108, x) or not d(x, y)) or ((x + y) > 80) or (A - y > x)):
                flag = False
            if not flag:
                break
    if flag:
        print(A)



