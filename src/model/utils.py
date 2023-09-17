import re

# Scheme sync
TIME_START = 0
TIME_END = 1
TIME = 2
WORD = 3
POS_START = 4
POS_END = 5
POS = 6

# Scheme sync_v2
L_POS = 0
R_POS = 1
L_WORDS = 2
R_WORDS = 3
L_a = 4
L_b = 5

# Scheme options
LOCALE = "locale"
DHT = False
PRELOAD = True
FG = "fg"
BG = "bg"
SEL = "sel"
FONT = "font"
FONTSIZE = "fontsize"
POSITIONS = "positions"
POSI = "posi"
AUDIO = "audio"


def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)


def time_format_srt(time):
    time = float(time)
    milli = time % 1
    time = time - milli
    milli = int(str(milli * 1000).split(".")[0])
    minute, second = divmod(time, 60)
    hour, minute = divmod(minute, 60)
    return '{:02.0f}:{:02.0f}:{:02.0f},{}'.format(hour, minute, second, milli)


def text2html(text,
              pattern=r'("?”?.+?)(\.\.\.?|\.\)?|!\.?\.?|\?\.?\.?|\n\n)',
              replacepattern=r'<p>\1\2</p>'):
    text1 = text[:].replace('"', ' ')
    text1 = text1.replace('”', ' ')
    result = re.sub(pattern, replacepattern, text1,
                    flags=re.DOTALL | re.UNICODE)
    return f"<html>{result}</html>"


barrier = 0.0


def find_max_sum(alist, a=0, b=0, sum_path=0, path=None):
    if path is None:
        path = []
    while (a < len(alist)) and (b < len(alist[a])):
        if alist[a][b] > barrier:
            path.append({"a": a, "b": b, "s": sum_path + alist[a][b]})
            b += 1
        else:
            try:
                if alist[a + 1][b + 1] > barrier:
                    a += 1
                    b += 1
                    continue
            except IndexError:
                pass
            diag_a = a + 1
            diag_b = b + 1
            diag_i = 1
            while (diag_a + diag_i < len(alist)) and (diag_b + diag_i < len(alist[diag_a])):
                if alist[diag_a + diag_i][diag_b + diag_i] > barrier:
                    diag_a = diag_a + diag_i
                    diag_b = diag_b + diag_i
                    diag_i += 1
                    break
                diag_i += 1
            check = []
            for j in range(b + 1, len(alist[a])):
                if alist[a][j] > barrier:
                    check.append({"a": a, "b": j, "s": sum_path + alist[a][j]})
                    break
            if not check:
                a += 1
                continue
            i = a + 1
            while i < len(alist):
                if alist[i][b] > barrier:
                    check.append({"a": i, "b": b, "s": sum_path + alist[i][b]})
                    break
                i += 1
            path_result = []
            for c in check:
                path_new = path[:]
                path_new.append({"a": c["a"], "b": c["b"], "s": c["s"]})
                path_result.append(find_max_sum(alist, c["a"] + 1, c["b"] + 1, c["s"], path_new))
            if diag_i != 1:
                path_result.append(find_max_sum(alist, diag_a, diag_b, sum_path, path))
            maximum = 0.0
            max_path = []
            for p in path_result:
                if len(p) > 0:
                    if p[-1]["s"] > maximum:
                        maximum = p[-1]["s"]
                        max_path = p[:]
            if max_path:
                return max_path
        a += 1
    return path


def find_max_path(alist, a=0, b=0, path=None):
    if path is None:
        path = []
    while (a < len(alist)) and (b < len(alist[a])):
        if alist[a][b] == 100:
            path.append({"a": a, "b": b})
            b += 1
        else:
            try:
                if alist[a + 1][b + 1] == 100:
                    a += 1
                    b += 1
                    continue
            except IndexError:
                pass
            diag_a = a + 1
            diag_b = b + 1
            diag_i = 1
            while (diag_a + diag_i < len(alist)) and (diag_b + diag_i < len(alist[diag_a])):
                if alist[diag_a + diag_i][diag_b + diag_i] == 100:
                    diag_a = diag_a + diag_i
                    diag_b = diag_b + diag_i
                    diag_i += 1
                    break
                diag_i += 1
            check = []
            for j in range(b + 1, len(alist[a])):
                if alist[a][j] == 100:
                    check.append({"a": a, "b": j})
                    break
            if not check:
                a += 1
                continue
            i = a + 1
            while i < len(alist):
                if alist[i][b] == 100:
                    check.append({"a": i, "b": b})
                    break
                i += 1
            path_result = []
            for c in check:
                path_new = path[:]
                path_new.append({"a": c["a"], "b": c["b"]})
                path_result.append(find_max_path(alist, c["a"] + 1, c["b"] + 1, path_new))
            if diag_i != 1:
                path_result.append(find_max_path(alist, diag_a, diag_b, path))
            maximum = 0
            max_path = []
            for p in path_result:
                if len(p) > maximum:
                    maximum = len(p)
                    max_path = p[:]
            if max_path:
                return max_path
        a += 1
    return path


def distance(mx, my, a, b):
    return abs(b * my + a * mx) / ((a * a + b * b) ** 0.5)


def find_max_path_v2(array):
    buffer = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 100:
                buffer.append((distance(j, i, -len(array), len(array[i])), j, i))
                array[i][j] = 0
    buffer.sort()
    path = []
    for x in buffer[0:20 * int((len(array) ** 2 + len(array[0]) ** 2) ** 0.5)]:
        path.append((x[1], x[2]))
    path.sort()
    result = []
    for p in path:
        result.append({"a": p[1], "b": p[0]})
        array[p[1]][p[0]] = 1
    return array


def dijkstra_max_path(alist):
    a = 0
    b = 0
    nodes = [[]]
    for i in range(1, len(alist)):
        for j in range(1, len(alist[i])):
            if alist[i][j] == 100:
                nodes[0].append({"a": a, "b": b, "i": i, "j": j})

    while True:
        nodes2 = []
        for c in range(len(nodes[-1])):
            for i in range(nodes[-1][c]["i"] + 1, len(alist)):
                for j in range(nodes[-1][c]["j"] + 1, len(alist[i])):
                    if alist[i][j] == 100:
                        nodes2.append({"a": nodes[-1][c]["i"], "b": nodes[-1][c]["j"], "i": i, "j": j})
        if not nodes2:
            break
        nodes.append(nodes2)
    paths = []
    for i in range(len(nodes[0])):
        nodes[0][i]["s"] = ((nodes[0][i]["i"] - nodes[0][i]["a"]) ** 2 +
                            (nodes[0][i]["j"] - nodes[0][i]["b"]) ** 2) ** 0.5
        paths.append([])
        paths[-1].append(nodes[0][i])
        for j in range(1, len(nodes[0])):
            try:
                nodes[j][i]["s"] = nodes[0][i]["s"] + \
                                   ((nodes[j][i]["i"] - nodes[j][i]["a"]) ** 2 +
                                    (nodes[j][i]["j"] - nodes[j][i]["b"]) ** 2) ** 0.5
                paths[-1].append(nodes[j][i])
            except IndexError:
                pass
    maximum = 0
    for i in range(len(paths)):
        if len(paths[i]) > maximum:
            maximum = len(paths[i])
    minimum = 10 ** 9
    if len(paths) == 0:
        return []
    index = 0
    for i in range(len(paths)):
        if len(paths[i]) == maximum:
            if minimum > paths[i][-1]["s"]:
                minimum = paths[i][-1]["s"]
                index = i
    return paths[index]


def r_map(data):
    r_start = []
    r_end = []
    r_word = []
    for i in data["fragments"]:
        try:
            for k in i["result"]:
                r_start.append(k["start"])
                r_end.append(k["end"])
                r_word.append(k["word"].lower().replace("ё", "е"))
        except KeyError:
            pass

    return r_start, r_end, r_word


def get_luminance(hex_color):
    color = hex_color[1:]
    hex_red = int(color[0:2], base=16)
    hex_green = int(color[2:4], base=16)
    hex_blue = int(color[4:6], base=16)
    return hex_red * 0.2126 + hex_green * 0.7152 + hex_blue * 0.0722


def color_contrast(hex_color):
    luminance = get_luminance(hex_color=hex_color)
    if luminance < 140:
        return "white"
    else:
        return "black"
