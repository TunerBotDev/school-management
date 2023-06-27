import sys
from datetime import datetime
import calendar
import json
auth_passed = False
def find_student_index(admission_number):
    with open("data.txt", "r") as file:
        existing_data = json.load(file)
    for i, student in enumerate(existing_data):
        if student["admission_number"] == admission_number:
            return i
    return -1


def display_student_data(student):
    print("Name:", student["name"])
    print("Class:", student["class"])
    print("Admission Number:", student["admission_number"])
    print("Age:", student["age"])
    grades = student["grades"]
    nlist = []
    for item in grades:
        nlist.append(item["name"])
    grades = ", ".join(nlist)
    print("Grades:", grades)
    print("Fees:", student["fees"])
    print("Joined On:", student["joined_on"])
    print("Next Due:", student["next_due"])
    print("Transport:", student["transport"])
    print()
def interface():
    global auth_passed
    print("[WELCOME] Welcome to The School Dashboard!")
    password = "school@2023_xyz"
    if auth_passed != True:
        authentication = input("Enter The Dashboard Password: ")
        if authentication != password:
            print("Invalid Password!")
            print("Terminating The Current Process.....")
            sys.exit()
        else: # Authentication passed.
            print("Authentication Passed!")
    print("What Would You Like To Do Today?\n1. Add A New Student\n2. Modify A Current Student.\n3. Get Information About Student\n4. Remove A Student")
    choice = int(input("Enter Your Choice: "))
    if choice not in range(1, 5):
        print("Invalid Choice Provided! Please Provide an Integer in the range from 1 to 4")
    elif choice == 1:
        # Create A New Student Data.
        student_entry = {}
        name = input("Enter The Name of Student: ")
        student_entry["name"] = name
        class_ = input("Enter The Class of Student: ")
        student_entry["class"] = class_
        admission_number = input("Enter The Student's Admission Number: ")
        with open("data.txt", "r") as file:
            info = json.load(file)
            for item in info:
                if isinstance(item, dict) and "admission_number" in item and item["admission_number"] == admission_number:
                    print("[ERROR]: A Student Already Exists With The Same Admission Number.")
                    sys.exit()
        student_entry["admission_number"] = admission_number
        age = input("Enter Student's Age: ")
        student_entry["age"] = age
        student_entry["grades"] = []
        # Get the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        student_entry["fees"] = current_datetime
        student_entry["joined_on"] = current_datetime
        current_month = datetime.now().month
        if current_month >= 12:
            current_month = 0
            # to bypass the extra months bug
        month_name = calendar.month_name[current_month]
        student_entry["next_due"] = month_name
        transport = input("Enter The Childern's Transport (School/Private): ")
        if transport not in ["School", "Private"]:
            print("Invalid Information Provided!")
            sys.exit()
        student_entry["transport"] = transport
        # Fetching the data.
        try:
            with open("data.txt", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []
        existing_data.append(student_entry)
        with open("data.txt", "w") as file:
            json.dump(existing_data, file)
        print("Added", name, "to Our School Database.")
        toggle = input("Do You Wish To Continue? (y/n): ")
        if toggle == "y":
            interface()
        else:
            sys.exit()
    elif choice == 2:
        with open("data.txt", "r") as file:
            existing_data = json.load(file)

        admission_number = input("Enter admission number of the student: ")
        student_index = find_student_index(admission_number)

        # Check if student exists
        if student_index != -1:
            # Get the student data
            student = existing_data[student_index]

            # Display the student data
            print("Student Data:")
            print("--------------")
            display_student_data(student)

            # Choose field to modify
            field = input("Enter the field you want to modify (e.g., age, grades, fees): ")

            # Check if the chosen field exists
            if field in student and field != "grades":
                # Modify the field
                new_value = input(f"Enter new value for {field}: ")
                student[field] = new_value

                # Save updated data to file
                with open("data.txt", "w") as file:
                    json.dump(existing_data, file)
                print("Data successfully updated.")
            elif field in student and field == "grades":
                exam = {}
                exname = input("Enter The Name of Exam: ")
                exam["name"] = exname
                maths = int(input("Enter The Grades in Mathematics: "))
                chemistry = int(input("Enter The Grades in Chemistry: "))
                physics = int(input("Enter The Grades in Physics: "))
                english = int(input("Enter The Grades in English: "))
                optional = int(input("Enter The Grades in Optional Subject: "))
                exam["maths"] = maths
                exam["chemistry"] = chemistry
                exam["physics"] = physics
                exam["english"] = english
                exam["optional"] = optional
                # Exam Dictonary Generated, Now time to store it.
                student["grades"].append(exam)

                with open("data.txt", "w") as file:
                    json.dump(existing_data, file)
                print("Data successfully updated.")
                toggle = input("Do You Wish To Continue? (y/n): ")
                if toggle == "y":
                    interface()
                else:
                    sys.exit()
            else:
                print("Entry Not Found.")
        else:
            print("Student not found.")
            sys.exit()
    elif choice == 3:
        with open("data.txt", "r") as file:
            existing_data = json.load(file)

        admission_number = input("Enter admission number of the student: ")
        student_index = find_student_index(admission_number)

        # Check if student exists
        if student_index != -1:
            # Get the student data
            student = existing_data[student_index]

            # Display the student data
            print("Student Data:")
            print("--------------")
            display_student_data(student)

            # Choose information to fetch
            info_choice = input("Enter the information you want to fetch (e.g., fees, next_due, transport): ")

            # Check if the chosen information exists
            if info_choice in student and info_choice != "grades":
                info_value = student[info_choice]
                print(f"{info_choice.capitalize()}: {info_value}")
                toggle = input("Do You Wish To Continue? (y/n): ")
                if toggle == "y":
                    interface()
                else:
                    sys.exit()
            elif info_choice in student and info_choice == "grades":
                what_type = input("What Exam's Grades You Wish To Know?: ")
                info_value = student["grades"]
                found = False
                for exam in info_value:
                    if exam["name"] == what_type:
                        found = True
                        print("The Grades For", what_type, "Are:\nMathematics:", exam["maths"], "\nChemistry:", exam["chemistry"], "\nPhysics:", exam["physics"], "\nEnglish:", exam["english"], "\nOptional:", exam["optional"])
                if found == False:
                    print("Unable to find an exam with that name!")
                    sys.exit()
            else:
                print("Invalid information.")
        else:
            print("Student not found.")
            sys.exit()
    elif choice == 4:
        admission_number_ = input("Enter The Admission Number of The Student You Wish To Remove: ")
        # Delete An Student Data
        with open("data.txt", "r") as file:
            data = json.load(file)
        # Find the index of the dictionary with the specified admission number
        index = -1
        for i, student in enumerate(data):
            if "admission_number" in student and student["admission_number"] == admission_number_:
                index = i
                break

        # Remove the dictionary from the list if found
        if index != -1:
            del data[index]
            print("Student removed successfully.")
        else:
            print("Student not found.")

        # Write the updated data back to the file
        with open("data.txt", "w") as file:
            json.dump(data, file)
interface()
