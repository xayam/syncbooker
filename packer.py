import os.path
import re
from src.app import Application
import zipfile


def pack(conf):
    application = Application(debug=True)
    for file_packer in conf:
        zip_path = f"data/{application.NAME}_v{application.VERSION}{conf[file_packer]}.zip"
        if os.path.exists(zip_path):
            print(f"ERROR: Path exists '{zip_path}'")
            continue
        with zipfile.ZipFile(zip_path,
                             mode='w',
                             compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            for dirname, _, files in os.walk("."):
                for filename in files:
                    file = os.path.join(dirname, filename)
                    changed = file.replace("\\", "/")[2:]
                    with open(file_packer, mode="r") as f:
                        patterns = f.readlines()
                    for p in patterns:
                        result = re.findall(r"^" + p.strip() + r"$", changed)
                        if result:
                            zf.write(os.path.join(dirname, filename))
                            print(os.path.join(dirname, filename))
                            break


if __name__ == "__main__":
    pack(conf={
               ".portable": ".Portable.Edition",
               ".offline": ".Offline.Edition",
               # ".developer": ".Developer.Edition"
    }
    )
