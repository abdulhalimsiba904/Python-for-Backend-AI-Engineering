import os

app_name = os.getenv("APP_NAME", "Python Data Toolkit")
output_dir = os.getenv("OUTPUT_DIR", "output")

print("Application:", app_name)
print("Output directory:", output_dir)