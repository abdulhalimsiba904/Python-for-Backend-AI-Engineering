file_path = "samples/notes.txt"

with open(file_path, "r", encoding="utf-8") as file:
    contents = file.read()

print(contents)