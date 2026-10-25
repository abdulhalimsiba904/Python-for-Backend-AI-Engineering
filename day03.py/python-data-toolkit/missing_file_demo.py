from pathlib import Path

file_path = Path("samples/not_here.json")

try:
    with file_path.open("r", encoding="utf-8") as file:
        contents = file.read()

except FileNotFoundError:
    print(f"Error: The file was not found: {file_path}")

else:
    print(contents)

print("Program continues.")