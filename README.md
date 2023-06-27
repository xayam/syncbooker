# SyncBooker

https://github.com/xayam/syncbooker

# Audio player for
- create
- viewing
- and listening two books: russian and english 
- on two language: russian and english
- catalog audiobooks are included

# List of books:
- Wells H.G. The Time Machine 

# Binary download
https://cloud.mail.ru/public/rdBB/KHvCjQdaT

# Development installation:
- install python 3.7+ (tested only version 3.7)
- create virtual enviroment in folder /venv
- run command for venv "python.exe -m pip install --upgrade pip"
- run command "pip install -r requirements-dev.txt"
- create folders "/modelrus" and "/modeleng"
  and unzip in this folders models from link https://alphacephei.com/vosk/models (russian and english model, 1.8GB each)
  
# For create own sync book:
- put files .mp3 in folders "/data/AUTHOR_-_NAME_BOOK/mp3rus/" and "/data/AUTHOR_-_NAME_BOOK/mp3eng/"
- put files rus.fb2, eng.fb2, rus.txt, eng.txt, cover.jpg, rus.annot.txt, eng.annot.txt in folder "/data/AUTHOR_-_NAME_BOOK/"
- run command in venv "python.exe createsync.py"
- if after last command exist file "/data/AUTHOR_-_NAME_BOOK/valid" - this success, sync book created!
