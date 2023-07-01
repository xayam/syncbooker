import json
import os
import time
from rapidfuzz import process, fuzz
from PIL import Image
import numpy as np
from consts import *


class Sync:
    def __init__(self, output, language):
        self.output = output
        np.set_printoptions(threshold=np.inf)
        self.MAPJSON = f"{self.output}/{language}.map.json"
        self.SYNCJSON = f"{self.output}/{language}.sync.json"
        self.TWOSYNC = f"{self.output}/two.json"
        mapjson = open(self.MAPJSON, mode="r", encoding="UTF-8")
        self.data = json.load(mapjson)
        mapjson.close()
        self.language = language

    def create_sync(self, synchronize, L_start, L_end, L_word, R_start, R_end, R_word):
        img = Image.fromarray(np.uint8(synchronize * 2.55), 'L')
        img.save(f"{self.output}/{self.language}.sync.png")
        sync = []
        L = 0
        R = 0
        L_window = 50
        R_window = int(L_window * (len(R_word) / len(L_word)))
        maxtime = {"max_time": 0, "L": L, "R": R}
        if not os.path.exists(self.SYNCJSON):
            print("Not find file self.SYNCJSON, creating...")
            while (L < len(L_word)) and (R < len(R_word)):
                # scores = process.cdist(L_chunk, R_chunk, scorer=fuzz.ratio,
                #                        dtype=np.uint8, score_cutoff=100)
                t1 = time.perf_counter()
                p = find_max_path(synchronize[L:L + L_window, R:R + R_window])
                # p = dijkstra_max_path(synchronize[L:L + L_window, R:R + R_window])
                t2 = time.perf_counter()
                # print(t2-t1)
                # break
                if t2 - t1 > maxtime["max_time"]:
                    maxtime = {"max_time": t2 - t1, "L": L, "R": R}
                a = -1
                b = -1
                for i in p:
                    a = i["a"]
                    b = i["b"]
                    sync.append([R_start[R + b],
                                 R_end[R + b],
                                 R + b,
                                 L_word[L + a],
                                 L_start[L + a],
                                 L_end[L + a],
                                 L + a])
                    print(L_word[L + a], R_word[R + b], sep="|||")
                if (a == -1) or (b == -1):
                    break
                L = L + a + 1
                R = R + b + 1
                print(f"L={L}, R={R}, POS_START={sync[-1][POS_START]}, TIME_START={sync[-1][TIME_START]}")
                print(maxtime)
                # break
            json_string = json.dumps(sync)
            with open(self.SYNCJSON, mode="w") as fsync:
                fsync.write(json_string)

        print("Find file self.SYNCJSON")
        with open(self.SYNCJSON, mode="r") as fsync:
            sync = json.load(fsync)

        print(f"len(L_word)={len(L_word)}")
        print(f"len(R_word)={len(R_word)}")
        print(f"len(sync)={len(sync)}")

        return sync

    def create_sync_v2(self, synchronize, L_word, R_word,L_end, R_end, L_len, R_len):
        sync1 = []
        L = 0
        R = 0
        L_window = 50
        R_window = int(L_window * (len(R_word) / len(L_word)))
        maxtime = {"max_time": 0, "L": L, "R": R}
        if True:
            while (L < len(L_word)) and (R < len(R_word)):
                t1 = time.perf_counter()
                # p = dijkstra_max_path(synchronize[L:L + L_window, R:R + R_window])
                p = find_max_path(synchronize[L:L + L_window, R:R + R_window])
                t2 = time.perf_counter()
                if t2 - t1 > maxtime["max_time"]:
                    maxtime = {"max_time": t2 - t1, "L": L, "R": R}
                a = -1
                b = -1
                for i in p:
                    a = i["a"]
                    b = i["b"]
                    sync1.append([L_end[L + a],
                                  R_end[R + b],
                                  L_word[L + a],
                                  R_word[R + b],
                                  L + a,
                                  R + b])
                    print(sync1[-1][L_POS], sync1[-1][R_POS], sep="::")
                    print(sync1[-1][L_WORDS])
                    print(sync1[-1][R_WORDS])
                if (a == -1) or (b == -1):
                    break
                L = L + a + 1
                R = R + b + 1
                print(f"L={L}, R={R}")
                print(maxtime)
        sync1.append([L_len,
                      R_len,
                      "",
                      "",
                      L - 1,
                      R - 1])
        print(sync1[-1][L_POS], sync1[-1][R_POS], sep="::")
        print(sync1[-1][L_WORDS])
        print(sync1[-1][R_WORDS])

        print(f"len(L_word)={len(L_word)}")
        print(f"len(R_word)={len(R_word)}")
        print(f"len(sync)={len(sync1)}")

        return sync1
