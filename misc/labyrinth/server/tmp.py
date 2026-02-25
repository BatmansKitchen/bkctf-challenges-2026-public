flag = "bkctf{y0ure_g0nn4_g3t_th3_h0rns}"
key_arr = []
legal = '0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}'
MIN = 0
MAX = len(legal) - 1
correct_path = ''

def ord(c):
    return legal.index(c)    

def chr(i):
    return legal[i]


print (ord('a'))

def solve(target, low, high, path):
    mid = (low + high) // 2
    # print (low, mid, high)
    if low == high:
        return low, path

    if ord(target) > mid:
        return solve(target, mid + 1, high, path + 'a')
    else:
        return solve(target, low, mid, path + 'b')


def search(key):
    low = MIN
    high = MAX

    for move in key:
        mid = (low + high) // 2

        # print (low, mid, high)
        if ord(move) % 2 == 0:
            high = mid
        elif ord(move) % 2 == 1:
            low = mid + 1
        else:
            raise ValueError('fuck')

    if low != high:
        return 0
    return low

for i in flag:
    res, correct_path = solve(i, MIN, MAX, '')
    print (res, chr(res), correct_path)
    res = search(correct_path)
    print (res, chr(res), correct_path)
    key_arr.append(correct_path)
print (key_arr)

# for i in range(len(flag)):
#     if i < len(key_arr): res = search(key_arr[i])
#     else: res = search('bbbaa')
#     print (f"goal: {ord(flag[i])} {flag[i]}, res: {res} {chr(res)}")