import json
import os
import sys
import audio
import recognizer
import sync
import translator
import similarity


folder_of_books = os.listdir("data")
for book in folder_of_books:
    if os.path.exists(f"data/{book}/valid"):
        with open(f"data/{book}/valid", mode="r", encoding="UTF-8") as f:
            valid = f.read()
        if valid == "True":
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
    audio.AudioClass(audio_list=mp3rus, output=f"data/{book}", language="rus")

    print(mp3eng)
    audio.AudioClass(audio_list=mp3eng, output=f"data/{book}", language="eng")

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

    Syncrus = sync.Sync(output=f"data/{book}", language="rus", book=rus_txt)
    SyncRus = Syncrus.create_sync()

    Synceng = sync.Sync(output=f"data/{book}", language="eng", book=eng_txt)
    SyncEng = Synceng.create_sync()

    trans = translator.Translator()
    orig_html = trans.text2html(text=rus_txt)
    if not os.path.exists(f"data/{book}/orig.html"):
        with open(f"data/{book}/orig.html", mode="w", encoding="UTF-8") as f:
            f.write(orig_html)

    if not os.path.exists(f"data/{book}/rus.html") or \
       not os.path.exists(f"data/{book}/eng.html"):
        rus_html, eng_html = trans.translate(text=eng_txt)
        with open(f"data/{book}/rus.html", mode="w", encoding="UTF-8") as f:
            f.write(rus_html)
        with open(f"data/{book}/eng.html", mode="w", encoding="UTF-8") as f:
            f.write(eng_html)
    else:
        with open(f"data/{book}/rus.html", mode="r", encoding="UTF-8") as f:
            rus_html = f.read()
        with open(f"data/{book}/eng.html", mode="r", encoding="UTF-8") as f:
            eng_html = f.read()

    trans = translator.Translator(from_code="ru", to_code="en")
    orig_html2 = trans.text2html(text=eng_txt)
    if not os.path.exists(f"data/{book}/orig2.html"):
        with open(f"data/{book}/orig2.html", mode="w", encoding="UTF-8") as f:
            f.write(orig_html2)

    if not os.path.exists(f"data/{book}/rus2.html") or \
       not os.path.exists(f"data/{book}/eng2.html"):
        eng_html2, rus_html2 = trans.translate(text=rus_txt)
        with open(f"data/{book}/rus2.html", mode="w", encoding="UTF-8") as f:
            f.write(rus_html2)
        with open(f"data/{book}/eng2.html", mode="w", encoding="UTF-8") as f:
            f.write(eng_html2)
    else:
        with open(f"data/{book}/rus2.html", mode="r", encoding="UTF-8") as f:
            rus_html2 = f.read()
        with open(f"data/{book}/eng2.html", mode="r", encoding="UTF-8") as f:
            eng_html2 = f.read()

    sem = similarity.Similarity(orig_html=orig_html, html=rus_html, d2v=os.getcwd() + f"/data/{book}/d2v.model")
    synchronize, L_word, R_word = sem.train()
    # img = Image.fromarray(np.uint8(synchronize * 255), 'L')
    # img.save("print1.png")
    if not os.path.exists(f"data/{book}/two.json"):
        print("Not find file two.json, creating...")
        two_sync = Syncrus.create_sync_v2(synchronize, L_word, R_word)
        json_string = json.dumps(two_sync)
        with open(f"data/{book}/two.json", mode="w") as fsync:
            fsync.write(json_string)
    else:
        print("Find file two.json")
        with open(f"data/{book}/two.json", mode="r") as fsync:
            two_sync = json.load(fsync)

    sem = similarity.Similarity(orig_html=orig_html2, html=eng_html2, d2v=os.getcwd() + f"/data/{book}/d2v2.model")
    synchronize, L_word, R_word = sem.train()
    # img = Image.fromarray(np.uint8(synchronize * 255), 'L')
    # img.save("print2.png")
    if not os.path.exists(f"data/{book}/two2.json"):
        print("Not find file two2.json, creating...")
        two_sync = Syncrus.create_sync_v2(synchronize, L_word, R_word)
        json_string = json.dumps(two_sync)
        with open(f"data/{book}/two2.json", mode="w") as fsync:
            fsync.write(json_string)
    else:
        print("Find file two2.json")
        with open(f"data/{book}/two2.json", mode="r") as fsync:
            two_sync = json.load(fsync)

    with open(f"data/{book}/valid", mode="w", encoding="UTF-8") as f:
        f.write("True")
