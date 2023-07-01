import os
import wave
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, model_path, output, language):
        self.language = language
        self.MAPJSON = f"{output}/{language}.map.json"
        self.WAV = f"{output}/{language}.wav"
        self.MODEL_PATH = model_path

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            print("Find file self.MAPJSON")
            return True
        wf = wave.open(self.WAV, "rb")
        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        ss = '{\n"fragments": [\n'
        while True:
            dat = wf.readframes(4000)
            if len(dat) == 0:
                break
            if rec.AcceptWaveform(dat):
                sss = rec.Result()
                ss += sss + ",\n"
                print(sss)
        ss += rec.FinalResult() + "]}"
        with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
            ff.write(ss)
        print("Create file self.MAPJSON")
        return True
