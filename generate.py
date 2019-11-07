import math, time, random
from captcha.captcha_process import captcha
seed = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnop~$^!|"

def charAt(s, pos):
    if pos < 0:
        return ""
    return s[pos]

def numberTransfer(a):
    b = seed
    c = b[:len(b)-3]
    d = len(c)
    e = b[-2]
    f = b[-3]
    g = f if a < 0 else ""
    a = abs(a)
    h = math.floor(a/d)
    i = [a % d, ]
    while h > 0:
        g = g + e
        i.append(h % d)
        h = math.floor(h / d)
    j = len(i) - 1

    while j >= 0:
        g = g + (charAt(c, i[j]) if 0==j else charAt(c, i[j]-1))
        j = j - 1
    if a < 0:
        g = f + g
    return g

def arrTransfer(a):
    b = [a[0], ]
    c = 0
    while c < len(a) - 1:
        d = []
        e = 0
        while e < len(a[c]):
            d.append(a[c+1][e] - a[c][e])
            e = e + 1
        c = c + 1
        b.append(d)
    return b

def qencode(a):
    b = seed[-1]
    c = arrTransfer(a)
    d = []
    e = []
    f = []
    g = 0
    while g < len(c):
        d.append(numberTransfer(c[g][0]))
        e.append(numberTransfer(c[g][1]))
        f.append(numberTransfer(c[g][2]))
        g = g + 1
    return "".join(d) + b + "".join(e) + b + "".join(f)

def generate_range(x, y, z):
    if (x == y):
        return [x] * z
    result = []
    d = (y-x)/z
    for i in range(z):
        result.append(int(x+d*i))
    return result

def generate_trace(trace = ['1', '2', '3', '4']):
    position = {'1': {'x': 30, 'y': 30},
                '2': {'x': 130, 'y': 30},
                '3': {'x': 30, 'y': 130},
                '4': {'x': 130, 'y':130},
                }
    trace_record = [[],[],[]]
    leap = 30
    for i in range(len(trace)-1):
        key_from, key_to = trace[i:i+2]
        pos_from, pos_to = position[key_from], position[key_to]
        trace_record[0] = trace_record[0] + list(generate_range(pos_from['x'], pos_to['x'], leap))
        trace_record[1] = trace_record[1] + list(generate_range(pos_from['y'], pos_to['y'], leap))
    trace_record[2] = list(generate_range(0, 2000, leap*3))
    trace_record[2][0] = int(time.time()*1000-1000)
    trace = []
    for i in range(len(trace_record[0])):
        trace.append([trace_record[0][i], trace_record[1][i], trace_record[2][i]])
    return trace

def generate_data_enc(img_data, mark):
    code = captcha(img_data, mark)
    if code is not None:
        trace = generate_trace(code)
        data_enc = qencode(trace)
        return (data_enc, code)
    else:
        return None

def generate_path_enc(a, b):
    c = len(b)-2
    d = b[c:]
    e = [0] * len(d)
    f = 0
    while f < len(d):
        g = ord(d[f])
        if g > 57:
            e[f] = g - 87
        else:
            e[f] = g - 48
        f = f + 1
    d = c * e[0] + e[1]
    i = int(a) + d
    j = b[0:c]
    k = [20, 50, 200, 500]
    l = []
    m = {}
    n = 0
    f = 0
    for o in k:
        l.append([])
    p = len(j)
    while p > f:
        h = charAt(j, f)
        if h not in m.keys() or m[h] is None or m[h] is False:
            m[h] = 1
            l[n].append(h)
            n = n + 1
            if n == len(l):
                n = 0
        f = f + 1
    r = i
    s = ""
    t = len(k) - 1
    while r > 0 and t >= 0:
        if r - k[t] >= 0:
            q = int(random.random() * len(l[t]))
            # print(q)
            # print(len(l[t]))
            s = s + l[t][q]
            r = r - k[t]
        else:
            t = t - 1
    return s

def generate_data_path_enc(img_data, mark, id):
    result = generate_data_enc(img_data, mark)
    if result is not None:
        data_enc, captcha_code = result
        captcha_code = "".join(captcha_code)
        path_enc = generate_path_enc(captcha_code, id)
        return [path_enc, data_enc, captcha_code]
    else:
        return None

if __name__ == '__main__':
    vid = "d7e62736326a55d543f10bee096350b3f6e096350b3f"
    code = "2134"
    # print(generate_path_enc(code, vid))
    print(generate_trace(['2', '1', '3', '4']))
    print(qencode(generate_trace(['2', '1', '3', '4'])))
    print(generate_path_enc(code, vid))



    # a = [
    #     [27, 32, 1542856188672], [28, 32, 30], [29, 32, 57], [30, 32, 72], [33, 32, 90], [37, 32, 107], [43, 32, 123],
    #     [50, 31, 140], [60, 30, 157], [66, 29, 173], [71, 28, 190], [75, 28, 206], [78, 28, 223], [83, 28, 240],
    #     [87, 28, 256], [90, 28, 273], [92, 28, 289], [95, 28, 307], [97, 28, 323], [99, 28, 340], [102, 28, 358],
    #     [104, 28, 374], [106, 29, 390], [107, 29, 407], [108, 29, 423], [108, 30, 440], [110, 30, 456], [111, 31, 473],
    #     [113, 33, 490], [117, 37, 507], [122, 41, 523], [126, 44, 540], [130, 46, 556], [132, 50, 574], [134, 53, 590],
    #     [136, 56, 607], [137, 61, 624], [138, 69, 641], [138, 77, 657], [139, 84, 673], [139, 91, 690], [139, 98, 707],
    #     [139, 102, 724], [139, 107, 740], [139, 110, 757], [139, 114, 773], [137, 119, 791], [135, 123, 807],
    #     [134, 125, 824], [133, 127, 841], [131, 128, 905], [129, 129, 923], [126, 130, 941], [122, 131, 957],
    #     [117, 131, 974], [111, 131, 988], [105, 131, 1007], [96, 131, 1024], [88, 131, 1038], [82, 131, 1056],
    #     [74, 131, 1074], [68, 131, 1090], [63, 131, 1107], [58, 131, 1124], [54, 129, 1140], [50, 129, 1157],
    #     [46, 128, 1173], [42, 128, 1190], [40, 128, 1206], [39, 128, 1224], [38, 128, 1241], [36, 128, 1273],
    #     [35, 128, 1291], [32, 128, 1308], [30, 128, 1324], [30, 128, 1552]
    # ]
    # print(encode(a))

    # b = "!)*^)^*^*^-^.^/^0^/^0^2^3^1^2^0^-^*(^)((((^)^,^)(^)(^)^)(^)(^)^*(((((()).4334111.,,,,.-)()(|M)*,/-//0.21120-*)))))^/^7^A^0^.^,^,^,^)^*^*^,^,^-^*^*^)^)^)^)^)*.32121/1.,-,--,))((|!!!!!!@IZFc*^!!!!!!@IZFb~C@6:99::9::9:?9:8AL9:!(SAH?:8:9?:8:::9?8:::9!(RCG:9:::99?9:9?99:d!06"
    # e = "!)*^)^*^*^-^.^/^0^/^0^2^3^1^2^0^-^*(^)((((^)^,^)(^)(^)^)(^)(^)^*(((((()).4334111.,,,,.-)()(|M)*,/-//0.21120-*)))))^/^7^A^0^.^,^,^,^)^*^*^,^,^-^*^*^)^)^)^)^)*.32121/1.,-,--,))((|!!!!!!@IZFc*^!!!!!!@IZFb~C@6:99::9::9:?9:8AL9:!(SAH?:8:9?:8:::9?8:::9!(RCG:9:::99?9:9?99:d!06"
    # d = "H))),-/03/.-,.-,*,**,**))(*)*-.--***))()((((((^*^*^)^)^*^*^,^-^.^/^/^2^1^/^1^/^.^.^-^-^-^-^*^)^)^*^)^,^*(|M((((((^)^)^)^)((((((((((()(()()*--,*-,,.11000-.,-.-**))))((((((((((^*(^)(((((((((|!!!!!!@IZL/FM^!!!!!!@IZL/F*H8?:9::9:9::9:9?9:?99:9:9:::9:9?9:::99:::9:9?9::$??9:7@:7??9::9:9:9?:M?:9!*N"
    # f = "H))),-/03/.-,.-,*,**,**))(*)*-.--***))()((((((^*^*^)^)^*^*^,^-^.^/^/^2^1^/^1^/^.^.^-^-^-^-^*^)^)^*^)^,^*(|M((((((^)^)^)^)((((((((((()(()()*--,*-,,.11000-.,-.-**))))((((((((((^*(^)(((((((((|!!!!!!@IZL/FM^!!!!!!@IZL/F*H8?:9::9:9::9:9?9:?99:9:9:::9:9?9:::99:::9:9?9::$??9:7@:7??9::9:9:9?:M?:9!*N"