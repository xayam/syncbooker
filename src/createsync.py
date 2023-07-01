import json
import os
import sys
import numpy as np
from PIL import Image
import audio
import recognizer
import sync
import cross
from consts import *


folder_of_books = os.listdir("data")
for book in folder_of_books:
    if os.path.exists(f"data/{book}/valid"):
        with open(f"data/{book}/valid", mode="r", encoding="UTF-8") as f:
            valid = f.read()
        if valid == "True":
            print(f"Book {book} is valid, continue...")
            continue
    if not os.path.exists(f"data/{book}/rus.txt"):
        print(f"Файла data/{book}/rus.txt не существует")
        sys.exit()
    with open(f"data/{book}/rus.txt", mode="r", encoding="UTF-8") as rus:
        rus_txt = rus.read()
    if not os.path.exists(f"data/{book}/eng.txt"):
        print(f"Файла data/{book}/eng.txt не существует")
        sys.exit()
    with open(f"data/{book}/eng.txt", mode="r", encoding="UTF-8") as eng:
        eng_txt = eng.read()
    mp3rus = [f"data/{book}/mp3rus/{x}" for x in os.listdir(f"data/{book}/mp3rus") if x[-4:] == ".mp3"]
    mp3eng = [f"data/{book}/mp3eng/{x}" for x in os.listdir(f"data/{book}/mp3eng") if x[-4:] == ".mp3"]
    print(mp3rus)
    audio.AudioClass(audio_list=mp3rus, output=os.getcwd() + f"/data/{book}", language="rus")
    print(mp3eng)
    audio.AudioClass(audio_list=mp3eng, output=os.getcwd() + f"/data/{book}", language="eng")
    delme = [f"data/{book}/{x}.bat" for x in ["audio", "wav", "flac"]]
    for d in delme:
        if os.path.exists(d):
            os.remove(d)

    RecognizerEng = recognizer.RecognizerClass(model_path=f"modeleng",
                                               output=f"data/{book}", language="eng")
    RecognizerEng.create_map()

    RecognizerRus = recognizer.RecognizerClass(model_path=f"modelrus",
                                               output=f"data/{book}", language="rus")
    RecognizerRus.create_map()

    if not os.path.exists(f"data/{book}/rus.sync.json"):
        mapjson = open(f"data/{book}/rus.map.json", mode="r", encoding="UTF-8")
        R_start, R_end, R_word = r_map(json.load(mapjson))
        mapjson.close()
        rus_html = text2html(text=rus_txt.lower(),
                             pattern=r'("?”?.+?)(\.\.\.?|\.\)?|!\.?\.?|\?\.?\.?|\n\n|,|:|;| |-)')
        if not os.path.exists(f"data/{book}/rus.html"):
            with open(f"data/{book}/rus.html", mode="w", encoding="UTF-8") as f:
                f.write(rus_html)
        synchronize, L_word, L_start, L_end = cross.get_sim(rus_html, R_word)
        Syncrus = sync.Sync(output=f"data/{book}", language="rus")
        two_sync = Syncrus.create_sync(synchronize, L_start, L_end, L_word, R_start, R_end, R_word)
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[POS]][i[TIME]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"data/{book}/rus2.sync.png")

    if not os.path.exists(f"data/{book}/eng.sync.json"):
        mapjson = open(f"data/{book}/eng.map.json", mode="r", encoding="UTF-8")
        R_start, R_end, R_word = r_map(json.load(mapjson))
        mapjson.close()
        eng_html = text2html(text=eng_txt.lower(),
                             pattern=r'("?”?.+?)(\.\.\.?|\.\)?|!\.?\.?|\?\.?\.?|\n\n|,|:|;| |-)')
        if not os.path.exists(f"data/{book}/eng.html"):
            with open(f"data/{book}/eng.html", mode="w", encoding="UTF-8") as f:
                f.write(eng_html)
        synchronize, L_word, L_start, L_end = cross.get_sim(eng_html, R_word)
        Synceng = sync.Sync(output=f"data/{book}", language="eng")
        two_sync = Synceng.create_sync(synchronize, L_start, L_end, L_word, R_start, R_end, R_word)
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[POS]][i[TIME]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"data/{book}/eng2.sync.png")

    if not os.path.exists(f"data/{book}/orig.html"):
        orig_html = text2html(text=rus_txt.lower(),
                              pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){8})',
                              replacepattern=r'<p>\1</p>')
        with open(f"data/{book}/orig.html", mode="w", encoding="UTF-8") as f:
            f.write(orig_html)

    if not os.path.exists(f"data/{book}/orig2.html"):
        orig_html2 = text2html(text=eng_txt.lower(),
                               pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){8})',
                               replacepattern=r'<p>\1</p>')
        with open(f"data/{book}/orig2.html", mode="w", encoding="UTF-8") as f:
            f.write(orig_html2)

    if not os.path.exists(f"data/{book}/two.json"):
        print("Not find file two.json, creating...")
        synchronize, L_word, R_word, L_end, R_end = cross.get_sim_v2(book)
        img = Image.fromarray(np.uint8(synchronize * 2.55), 'L')
        img.save(f"data/{book}/two.png")
        Syncrus = sync.Sync(output=f"data/{book}", language="rus")
        two_sync = Syncrus.create_sync_v2(synchronize, L_word, R_word, L_end, R_end,
                                          len(rus_txt) - 1, len(eng_txt) - 1)
        for i in range(len(synchronize)):
            for j in range(len(synchronize[i])):
                synchronize[i][j] = 0
        for i in two_sync:
            synchronize[i[L_a]][i[L_b]] = 255
        img = Image.fromarray(np.uint8(synchronize), 'L')
        img.save(f"data/{book}/two2.png")
        json_string = json.dumps(two_sync)
        with open(f"data/{book}/two.json", mode="w") as fsync:
            fsync.write(json_string)
    else:
        print("Find file two.json")
        with open(f"data/{book}/two.json", mode="r") as fsync:
            two_sync = json.load(fsync)

    with open(f"data/{book}/valid", mode="w", encoding="UTF-8") as f:
        f.write("True")
