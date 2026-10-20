
# personal_profile.py

print("=== PERSONAL PROFILE ===\n")

# Ask the user for information
name = input("Enter your name: ").strip()
age = int(input("Enter your age: "))
monthly_income = float(input("Enter your monthly income: "))

# Ask whether the user is a student and validate the answer
while True:
    student_answer = input(
        "Are you a student? (yes/y/no/n): "
    ).strip().lower()

    if student_answer in ("yes", "y"):
        is_student = True
        break
    elif student_answer in ("no", "n"):
        is_student = False
        break
    else:
        print("Invalid input. Please enter yes (y) or no (n).")

# Calculate annual income
annual_income = monthly_income * 12

# Show the summary
print("\n=== PROFILE SUMMARY ===")
print("Name:", name)
print("Age:", age)
print("Student:", is_student)
print("Monthly Income:", f"{monthly_income:.2f}")
print("Annual Income:", f"{annual_income:.2f}")

# Show the data types
print("\n=== DATA TYPES ===")
print("Name type:", type(name))
print("Age type:", type(age))
print("Student type:", type(is_student))
print("Monthly income type:", type(monthly_income))
print("Annual income type:", type(annual_income))
