import os
from pathlib import Path

output_dir = Path(os.getenv("OUTPUT_DIR", "output"))

output_dir.mkdir(parents=True, exist_ok=True)

report_file = output_dir / "report.txt"

print("Output directory:", output_dir.resolve())
print("Report path:", report_file.resolve())
print("Output directory exists:", output_dir.is_dir())