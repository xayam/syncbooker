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



draws = []


def time_format_srt(time):
    time = float(time)
    milli = time % 1
    time = time - milli
    milli = int(str(milli * 1000).split(".")[0])
    minute, second = divmod(time, 60)
    hour, minute = divmod(minute, 60)
    return '{:02.0f}:{:02.0f}:{:02.0f},{}'.format(hour, minute, second, milli)


arr = [
    [000, 000, 000, 000, 100, 000, 000],
    [000, 000, 000, 000, 000, 000, 000],
    [000, 000, 100, 000, 000, 000, 000],
    [100, 000, 000, 000, 000, 000, 000],
    [000, 000, 000, 000, 000, 000, 000],
    [000, 000, 000, 000, 000, 000, 000],
    [100, 000, 000, 000, 000, 000, 000],
    [000, 000, 000, 000, 000, 000, 100]]

barrier = 0.0


def find_max_sum(alist, a=0, b=0, sum=0, path=None):
    if path is None:
        path = []
    while (a < len(alist)) and (b < len(alist[a])):
        if alist[a][b] > barrier:
            path.append({"a": a, "b": b, "s": sum + alist[a][b]})
            b += 1
        else:
            try:
                if alist[a + 1][b + 1] > barrier:
                    a += 1
                    b += 1
                    continue
            except IndexError:
                pass
            diagA = a + 1
            diagB = b + 1
            diagI = 1
            while (diagA + diagI < len(alist)) and (diagB + diagI < len(alist[diagA])):
                if alist[diagA + diagI][diagB + diagI] > barrier:
                    diagA = diagA + diagI
                    diagB = diagB + diagI
                    diagI += 1
                    break
                diagI += 1
            check = []
            for j in range(b + 1, len(alist[a])):
                if alist[a][j] > barrier:
                    check.append({"a": a, "b": j, "s": sum + alist[a][j]})
                    break
            if not check:
                a += 1
                continue
            i = a + 1
            while i < len(alist):
                if alist[i][b] > barrier:
                    check.append({"a": i, "b": b, "s": sum + alist[i][b]})
                    break
                i += 1
            pathResult = []
            for c in check:
                pathNew = path[:]
                pathNew.append({"a": c["a"], "b": c["b"], "s": c["s"]})
                pathResult.append(find_max_sum(alist, c["a"] + 1, c["b"] + 1, c["s"], pathNew))
            if diagI != 1:
                pathResult.append(find_max_sum(alist, diagA, diagB, sum, path))
            maximum = 0
            maxpath = []
            for p in pathResult:
                if len(p) > maximum:
                    maximum = len(p)
                    maxpath = p[:]
            if maxpath:
                return maxpath
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
            diagA = a + 1
            diagB = b + 1
            diagI = 1
            while (diagA + diagI < len(alist)) and (diagB + diagI < len(alist[diagA])):
                if alist[diagA + diagI][diagB + diagI] == 100:
                    diagA = diagA + diagI
                    diagB = diagB + diagI
                    diagI += 1
                    break
                diagI += 1
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
            pathResult = []
            for c in check:
                pathNew = path[:]
                pathNew.append({"a": c["a"], "b": c["b"]})
                pathResult.append(find_max_path(alist, c["a"] + 1, c["b"] + 1, pathNew))
            if diagI != 1:
                pathResult.append(find_max_path(alist, diagA, diagB, path))
            maximum = 0
            maxpath = []
            for p in pathResult:
                if len(p) > maximum:
                    maximum = len(p)
                    maxpath = p[:]
            if maxpath:
                return maxpath
        a += 1
    return path


if __name__ == "__main__":
    print(find_max_path(arr))


def middle_time(sync):
    s = 0
    for i in sync:
        s += i["time"]
    return s // len(sync)


def check_min_max(s1, s2, s3):
    delta = 0
    return ((s2["time"] > s1["time"] + delta) and (s2["time"] > s3["time"] + delta)) or \
        ((s2["time"] < s1["time"] + delta) and (s2["time"] < s3["time"] + delta))


def check_min_max_v2(s1, s2, s3, s4):
    delta = 0
    return ((s2["time"] > s1["time"] + delta) and (s2["time"] > s4["time"] + delta) and
            (s3["time"] > s1["time"] + delta) and (s3["time"] > s4["time"] + delta)) or \
        ((s2["time"] < s1["time"] + delta) and (s2["time"] < s4["time"] + delta) and
         (s3["time"] < s1["time"] + delta) and (s3["time"] < s4["time"] + delta))


l_book_language = {"rus": {"+": "плюс", "1": "один", "2": "два", "3": "три", "4": "четыре", "5": "пять",
                           "6": "шесть", "7": "семь", "8": "восемь", "9": "девять"},
                   "eng": {"+": "plus", "1": "one", "2": "two", "3": "tree", "4": "four", "5": "five",
                           "6": "six", "7": "seven", "8": "eight", "9": "nine"}}


def l_book(book, language):
    b = book.lower().replace("ё", "е")
    L_start = []
    L_end = []
    L_word = []
    word = ''
    start = 0
    end = 0
    a = 0
    for char in b:
        if char == "+":
            if re.findall(r"\b\+\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "1":
            if re.findall(r"\b1\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "2":
            if re.findall(r"\b2\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "3":
            if re.findall(r"\b3\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "4":
            if re.findall(r"\b4\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "5":
            if re.findall(r"\b5\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "6":
            if re.findall(r"\b6\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "7":
            if re.findall(r"\b7\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "8":
            if re.findall(r"\b8\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char == "9":
            if re.findall(r"\b9\b", b[a - 1:a + 2]):
                word = l_book_language[language][char]
        if char in "йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm":
            word += char
            end += 1
        else:
            if word:
                L_start.append(start)
                L_end.append(end)
                L_word.append(word)
                word = ''
                start = end
            start += 1
            end += 1
        a += 1
    if word:
        L_start.append(start)
        L_end.append(end)
        L_word.append(word)

    return L_start, L_end, L_word


def r_map(data):
    R_start = []
    R_end = []
    R_word = []
    for i in data["fragments"]:
        try:
            for k in i["result"]:
                R_start.append(k["start"])
                R_end.append(k["end"])
                R_word.append(k["word"].lower().replace("ё", "е"))
        except KeyError:
            pass

    return R_start, R_end, R_word


def distance(x0, y0, x1, y1, x2, y2):
    return abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / (((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5)
