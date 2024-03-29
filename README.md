# SyncBooker

- Sources: https://github.com/xayam/syncbooker
- Telegram chat: https://t.me/syncbooker_chat
- Binary download: https://cloud.mail.ru/public/rdBB/KHvCjQdaT

# Audio player for

- create
- synchrone viewing
- and synchrone listening two books: russian and english 
- on two language: russian and english
- catalog audiobooks are included

# List of books:

- Kafka Franz The Metamorphosis
- Kuttner Henry The Ego Machine
- Lewis Carroll Alices Adventures in Wonderland
- Wells Herbert The Time Machine 

# Binary download

https://cloud.mail.ru/public/rdBB/KHvCjQdaT

# Development installation (for create own sync book):

- install python 3.7-3.9 (tested only version 3.9)
- creating virtual enviroment, run command "python.exe -m venv venv"
- activating venv, run command "venv/Scripts/activate.bat"
- upgrading pip, run command "python.exe -m pip install --upgrade pip"
- install requirements, run command "pip install -r requirements.txt"
- (if you not download binary "Developer Edition") create folders "/src/rus" and "/src/eng"
  and unzip in folders models from link https://alphacephei.com/vosk/models (russian and english model, 1.8GB each)
- install SOX for audio convert, unpack archive of program, 
  which you must download from link https://sourceforge.net/projects/sox/files/sox/ choose last version (I test on version sox 14.4.2)
- add SOX binary folder in PATH env
- install Graphviz for get scheme of project. After install run command in venv:
  "cd src" and
  "pyan3 **/*.py --uses --no-defines --colored --grouped --annotated --svg > app.svg"

# For create own sync book:

- put files .mp3 in folders "/data/AUTHOR_-_NAME_BOOK/mp3rus/" 
  and "/data/AUTHOR_-_NAME_BOOK/mp3eng/"
  
- put files rus.fb2, eng.fb2, rus.txt, eng.txt, cover.jpg, rus.annot.txt, eng.annot.txt 
  in folder "/data/AUTHOR_-_NAME_BOOK/"
  
- run command in venv "python.exe createsync.py"

- each launch of the "python.exe createsync.py" command must be done after the obligatory deletion of the /valid file, otherwise the processing will not be carried out

- check the quality. For this you must analisys next images: rus.sync.png, rus2.sync.png, eng.sync.png,  eng2.sync.png, two.png and two2.png. All these images should not contain large breaks on the main diagonal lines.

- if the rus.sync.png file contains breaks, then you should edit the text of the rus.txt file (if the gap is vertical) or mp3 files for the russian language (if the gap is horizontal)

- After that, if there were breaks and you fixed them in the files, you should delete the /valid, /rus.sync.json and /eng.sync.json files. And restart the command "python.exe createsync.py"

- check quality images rus.sync.png and eng.sync.png

- if there are no breaks in these files, then after that you need to check the two.png image for breaks in the main diagonal. If the gap is horizontal, then the eng.txt and english mp3 files contain pieces of text and audio that are not in the Russian version (delete them), delete rus.sync.json, delete eng.sync.json and restart createsync.py. If the gap is vertical, then the rus.txt and russian mp3 files contain pieces of text and audio that are not in the English version (delete them) and restart createsync.py

- if after that there are no big gaps in any of these files and after the last run of createsync.py there is a file /valid then I congratulate you creation of synchronous books is completed and the quality should be acceptable