import json
import os
import sys
import numpy as np
from PIL import Image, ImageDraw

import audio
import recognizer
import sync
import cross

from model.eps import *
from model.utils import *
from model.config import Config

config = Config()
data = "../../data"
folder_of_books = os.listdir(data)
for book in folder_of_books:
    if os.path.exists(f"{data}/{book}/{config.VALID}"):
        with open(f"{data}/{book}/{config.VALID}", mode="r", encoding="UTF-8") as f:
            valid = f.read()
        if valid == "True":
            print(f"Book {book} is valid, continue...")
            continue
    if not os.path.exists(f"{data}/{book}/{config.RUS_TXT}"):
        print(f"Файла {data}/{book}/{config.RUS_TXT} не существует")
        sys.exit()
    with open(f"{data}/{book}/{config.RUS_TXT}", mode="r", encoding="UTF-8") as rus:
        rus_txt = rus.read()
    if not os.path.exists(f"{data}/{book}/{config.ENG_TXT}"):
        print(f"Файла {data}/{book}/{config.ENG_TXT} не существует")
        sys.exit()
    with open(f"{data}/{book}/{config.ENG_TXT}", mode="r", encoding="UTF-8") as eng:
        eng_txt = eng.read()
    if not os.path.exists(os.getcwd() + f"/{data}/{book}/" + config.RUS_FLAC):
        mp3rus = [f"{data}/{book}/mp3rus/{x}" for x in os.listdir(f"{data}/{book}/mp3rus") if x[-4:] == ".mp3"]
        print(mp3rus)
        audio.AudioClass(audio_list=mp3rus, output=os.getcwd() + f"/{data}/{book}", language="rus")
    if not os.path.exists(os.getcwd() + f"/{data}/{book}/" + config.ENG_FLAC):
        mp3eng = [f"{data}/{book}/mp3eng/{x}" for x in os.listdir(f"{data}/{book}/mp3eng") if x[-4:] == ".mp3"]
        print(mp3eng)
        audio.AudioClass(audio_list=mp3eng, output=os.getcwd() + f"/{data}/{book}", language="eng")

    del_me = [f"{data}/{book}/{x}.bat" for x in ["audio", "wav", "flac"]]
    for d in del_me:
        if os.path.exists(d):
            os.remove(d)
    recognizer_eng = recognizer.RecognizerClass(model_path=f"../eng",
                                                output=f"{data}/{book}", language="eng")
    recognizer_eng.create_map()
    recognizer_rus = recognizer.RecognizerClass(model_path=f"../rus",
                                                output=f"{data}/{book}", language="rus")
    recognizer_rus.create_map()

    if not os.path.exists(f"{data}/{book}/{config.RUS_SYNC}"):
        with open(f"{data}/{book}/rus.map.json", mode="r", encoding="UTF-8") as map_json:
            R_start, R_end, R_word = r_map(json.load(map_json))
        rus_html = text2html(text=rus_txt.lower(),
                             pattern=r'([а-я0-9a-z]+)([^а-я0-9a-z]+)')
        if not os.path.exists(f"{data}/{book}/rus.html"):
            with open(f"{data}/{book}/rus.html", mode="w", encoding="UTF-8") as f:
                f.write(rus_html)
        synchronize, L_word, L_start, L_end = cross.get_sim(rus_html, R_word)
        sync_rus = sync.Sync(output=f"{data}/{book}", language="rus")
        two_sync = sync_rus.create_sync(synchronize, L_start, L_end, L_word, R_start, R_end, R_word)
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[POS]][i[TIME]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"{data}/{book}/rus2.sync.png")

    if not os.path.exists(f"{data}/{book}/{config.ENG_SYNC}"):
        with open(f"{data}/{book}/eng.map.json", mode="r", encoding="UTF-8") as map_json:
            R_start, R_end, R_word = r_map(json.load(map_json))
        eng_html = text2html(text=eng_txt.lower(),
                             pattern=r'([а-я0-9a-z]+)([^а-я0-9a-z]+)')
        if not os.path.exists(f"{data}/{book}/eng.html"):
            with open(f"{data}/{book}/eng.html", mode="w", encoding="UTF-8") as f:
                f.write(eng_html)
        synchronize, L_word, L_start, L_end = cross.get_sim(eng_html, R_word)
        sync_eng = sync.Sync(output=f"{data}/{book}", language="eng")
        two_sync = sync_eng.create_sync(synchronize, L_start, L_end, L_word, R_start, R_end, R_word)
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[POS]][i[TIME]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"{data}/{book}/eng2.sync.png")

    if not os.path.exists(f"{data}/{book}/{config.RUS_ORIG}"):
        orig_html = text2html(text=rus_txt.lower(),
                              pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){4})',
                              replacepattern=r'<p>\1</p>')
        with open(f"{data}/{book}/{config.RUS_ORIG}", mode="w", encoding="UTF-8") as f:
            f.write(orig_html)

    if not os.path.exists(f"{data}/{book}/{config.ENG_ORIG}"):
        orig_html2 = text2html(text=eng_txt.lower(),
                               pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){4})',
                               replacepattern=r'<p>\1</p>')
        with open(f"{data}/{book}/{config.ENG_ORIG}", mode="w", encoding="UTF-8") as f:
            f.write(orig_html2)

    sync_rus = sync.Sync(output=f"{data}/{book}", language="rus")
    if not os.path.exists(f"{data}/{book}/two.json"):
        print("Not find file two.json, creating...")
        synchronize, L_word, R_word, L_end, R_end = cross.get_sim_v2(book, data)
        synchronize = find_max_path_v2(synchronize)
        img = Image.fromarray(np.uint8(synchronize * 255), 'L')
        img.save(f"{data}/{book}/two.png")

        res_min_max = filtered_main_diag(f"{data}/{book}/two.png")
        synchronize = np.asarray(np.uint8(res_min_max * 100))
        res_min_max = Image.fromarray(np.uint8(res_min_max * 255))
        res_min_max.save(f"{data}/{book}/two2.png")
        two_sync = sync_rus.create_sync_v2(synchronize, L_word, R_word, L_end, R_end,
                                           len(L_word) - 1, len(R_word) - 1, append=False)
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[L_a]][i[L_b]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"{data}/{book}/two3.png")

        img1 = np.zeros_like(synchronize)
        img2 = Image.fromarray(img1)
        img = ImageDraw.Draw(img2)
        a = 0
        b = 0
        for i in range(len(two_sync)):
            img.line([(b, a), (two_sync[i][L_b], two_sync[i][L_a])], fill="white", width=0)
            a = two_sync[i][L_a]
            b = two_sync[i][L_b]
        img2.save(f"{data}/{book}/adapter.png")
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                img1[i][j] = int(img2.getpixel((j, i)) / 2.55)
        synchronize = np.asarray(img1)
        print("Recreate two_sync...")
        two_sync = sync_rus.create_sync_v2(synchronize, L_word, R_word, L_end, R_end,
                                           len(L_word) - 1, len(R_word) - 1,
                                           append=False,
                                           L_window=25)

        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[L_a]][i[L_b]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"{data}/{book}/adapter2.png")

        json_string = json.dumps(two_sync)
        with open(f"{data}/{book}/two.json", mode="w") as fsync:
            fsync.write(json_string)
    else:
        print("Find file two.json")
        with open(f"{data}/{book}/two.json", mode="r") as fsync:
            two_sync = json.load(fsync)

    if not os.path.exists(f"{data}/{book}/{config.MICRO_JSON}"):
        micro = []
        for i in two_sync:
            phraza_1 = i[2]
            phraza_2 = i[3]
            if phraza_1.strip() == '' or phraza_2.strip() == '':
                phraza_1 = 'и '
                phraza_2 = 'and '
            words1 = re.findall(r"[а-я0-9a-z]+[^а-я0-9a-z]+", phraza_1)
            words2 = re.findall(r"[а-я0-9a-z]+[^а-я0-9a-z]+", phraza_2)
            synchronize, L_word, R_word, L_end, R_end = cross.get_sim_v21(words1, words2)
            assert len(L_word) == len(R_word)
            two = sync_rus.create_sync_v3(synchronize, L_word, R_word, L_end, R_end,
                                          len(L_word), len(R_word), i)
            micro.append(two)
        index = -1
        micro2 = micro[:]
        for j in micro2:
            index += 1
            L_sync = two_sync[index][L_POS]
            R_sync = two_sync[index][R_POS]
            for k in range(len(micro[index]) - 1):
                L_delta = sum([len(t[L_WORDS]) for t in micro[index][k:]])
                R_delta = sum([len(t[R_WORDS]) for t in micro[index][k:]])
                micro[index][k][L_POS] = L_sync - L_delta
                micro[index][k][R_POS] = R_sync - R_delta
        micro[-1][-1][L_POS] = len(rus_txt) - 1
        micro[-1][-1][R_POS] = len(eng_txt) - 1
        json_string = json.dumps(micro)
        with open(f"{data}/{book}/{config.MICRO_JSON}", mode="w") as f:
            f.write(json_string)
    else:
        pass

    with open(f"{data}/{book}/{config.VALID}", mode="w", encoding="UTF-8") as f:
        f.write("True")
