from pathlib import Path

project_dir = Path(".")

samples_dir = project_dir / "samples"
transactions_file = samples_dir / "transactions.csv"

print("Project directory:", project_dir.resolve())
print("Samples directory:", samples_dir)
print("CSV file path:", transactions_file)
print("File exists:", transactions_file.exists())
print("Is a file:", transactions_file.is_file())
print("Is a directory:", samples_dir.is_dir())


#from pathlib import Path

output_dir = Path("output/reports")

output_dir.mkdir(parents=True, exist_ok=True)

print("Output directory:", output_dir.resolve())
print("Directory exists:", output_dir.is_dir())