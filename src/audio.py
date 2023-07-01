import os
from mutagen.mp3 import MP3


# from pydub import AudioSegment
# from tqdm import tqdm


class AudioClass:
    def __init__(self, audio_list, output, language):
        self.AUDIOBAT = f"{output}/audio.bat"
        self.WAVBAT = f"{output}/wav.bat"
        self.FLACBAT = f"{output}/flac.bat"
        self.MP3 = f"{output}/{language}.mp3"
        self.WAV = f"{output}/{language}.wav"
        self.FLAC = f"{output}/{language}.flac"
        self.audio_list = audio_list

        self.create_mp3()
        self.create_wav()
        self.create_flac()

    def create_wav(self):
        if os.path.exists(self.WAV):
            return
        print("Converting mp3 to wav...")
        s = "@echo off\n"
        s += "@chcp 65001\n"
        swav = s + \
               os.getcwd() + '/sox/sox.exe ' + \
               f'"{self.MP3}" "{self.WAV}" channels 1 rate 16k'
        with open(self.WAVBAT, mode="w", encoding="UTF-8") as wavbat:
            wavbat.write(swav)
            print("Create Config.WAVBAT")
        os.system(self.WAVBAT)

    def create_flac(self):
        if os.path.exists(self.FLAC):
            return
        print("Converting mp3 to flac...")
        s = "@echo off\n"
        s += "@chcp 65001\n"
        sflac = s + \
                os.getcwd() + '/sox/sox.exe ' + \
                f'"{self.MP3}" "{self.FLAC}" channels 1 rate 16k'
        with open(self.FLACBAT, mode="w", encoding="UTF-8") as flacbat:
            flacbat.write(sflac)
            print("Create Config.FLACBAT")
        os.system(self.FLACBAT)

    def create_mp3(self):
        if os.path.exists(self.MP3):
            return
        kk = 0
        ss = ''
        listing = ''
        listmp3 = ''
        for i in self.audio_list:
            ss += f'[{kk}]'
            listing += f"file '{i}'\n"
            listmp3 += f'"{i}" '
            audio1 = MP3(i)
            listing += f"duration {audio1.info.length}\n"
            kk += 1

        with open(self.AUDIOBAT, mode="w", encoding="UTF-8") as audiobat:
            listmp3 = "@echo off\n@chcp 65001\n" + \
                      os.getcwd() + "/sox/sox.exe " + listmp3 + \
                      f"{self.MP3}"
            audiobat.write(listmp3)
            print("Create AUDIOBAT")

        print("Running AUDIOBAT...")
        os.system(self.AUDIOBAT)
