import pathlib

PATH = pathlib.Path(__file__).parent
CORE = PATH / "core"

output = ""

for folder_ in CORE.iterdir():
    folder = pathlib.Path(folder_)
    for file in folder.iterdir():
        with open(file, "r", encoding="utf-8") as f:
            output += "file: " + folder.name + "/" + file.name + "\n"
            output += "".join(f.readlines())
            output += "\n\n\n"

with open("compiledcode.txt", "w", encoding="utf-8") as f:
    f.write(output)