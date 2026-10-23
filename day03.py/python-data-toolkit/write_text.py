file_path = "samples/report.txt"

report = "Daily Transaction Report\n"
report += "Total transactions: 3\n"
report += "Total amount: 225.00\n"

with open(file_path, "w", encoding="utf-8") as file:
    file.write(report)

print("Report saved successfully.")