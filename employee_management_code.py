import os
import struct

class Employee:
    def __init__(self):
        self.code = 0
        self.name = ""
        self.salary = 0.0

    def read(self):
        try:
            self.code = int(input("Enter employee code: "))
            self.name = input("Enter name: ")
            self.salary = float(input("Enter salary: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            self.read()

    def display(self):
        print(self.code, self.name, "\t", self.salary)


def delete_existing_file():
    if os.path.exists("EMPLOYEE.DAT"):
        os.remove("EMPLOYEE.DAT")


def append_to_file():
    x = Employee()
    x.read()

    with open("EMPLOYEE.DAT", "ab") as file:
        file.write(x.code.to_bytes(4, "little"))
        file.write(x.name.encode("utf-8"))
        file.write(b"\x00" * (20 - len(x.name)))
        file.write(struct.pack("f", x.salary))  # Convert float to bytes using struct.pack

    print("Record added successfully.")


def display_all():
    try:
        with open("EMPLOYEE.DAT", "rb") as file:
            while True:
                code_bytes = file.read(4)
                if not code_bytes:
                    break
                code = int.from_bytes(code_bytes, "little")
                name = file.read(20).decode("utf-8").rstrip("\x00")
                salary_bytes = file.read(4)
                salary = struct.unpack("f", salary_bytes)[0]  # Convert bytes to float using struct.unpack
                x = Employee()
                x.code = code
                x.name = name
                x.salary = salary
                if 1000 <= x.salary <= 200000:
                    x.display()
    except FileNotFoundError:
        print("EMPLOYEE.DAT file not found. No records to display.")


def search_for_record():
    try:
        c = int(input("Enter employee code: "))
        with open("EMPLOYEE.DAT", "rb") as file:
            while True:
                code_bytes = file.read(4)
                if not code_bytes:
                    break
                code = int.from_bytes(code_bytes, "little")
                name = file.read(20).decode("utf-8").rstrip("\x00")
                salary_bytes = file.read(4)
                salary = struct.unpack("f", salary_bytes)[0]  # Convert bytes to float using struct.unpack
                x = Employee()
                x.code = code
                x.name = name
                x.salary = salary
                if x.code == c:
                    print("RECORD FOUND")
                    x.display()
                    return
        print("Record not found!!!")
    except FileNotFoundError:
        print("EMPLOYEE.DAT file not found. No records to search.")


def increase_salary():
    try:
        c = int(input("Enter employee code: "))
        sal = float(input("Salary hike? "))

        with open("EMPLOYEE.DAT", "r+b") as file:
            while True:
                code_bytes = file.read(4)
                if not code_bytes:
                    break
                code = int.from_bytes(code_bytes, "little")
                name = file.read(20).decode("utf-8").rstrip("\x00")
                salary_bytes = file.read(4)
                salary = struct.unpack("f", salary_bytes)[0]  # Convert bytes to float using struct.unpack
                x = Employee()
                x.code = code
                x.name = name
                x.salary = salary
                if x.code == c:
                    x.salary += sal
                    file.seek(-4, 1)
                    file.write(struct.pack("f", x.salary))  # Convert float to bytes using struct.pack
                    print("Salary updated successfully.")
                    return
        print("Record not found!!!")
    except FileNotFoundError:
        print("EMPLOYEE.DAT file not found. Cannot update salary.")


def insert_record():
    try:
        new_emp = Employee()
        new_emp.read()

        with open("EMPLOYEE.DAT", "r+b") as file, open("TEMP.DAT", "wb") as fin:
            while True:
                code_bytes = file.read(4)
                if not code_bytes:
                    break
                code = int.from_bytes(code_bytes, "little")
                name = file.read(20).decode("utf-8").rstrip("\x00")
                salary_bytes = file.read(4)
                salary = struct.unpack("f", salary_bytes)[0]  # Convert bytes to float using struct.unpack
                x = Employee()
                x.code = code
                x.name = name
                x.salary = salary
                if x.code > new_emp.code:
                    fin.write(new_emp.code.to_bytes(4, "little"))
                    fin.write(new_emp.name.encode("utf-8"))
                    fin.write(b"\x00" * (20 - len(new_emp.name)))
                    fin.write(struct.pack("f", new_emp.salary))  # Convert float to bytes using struct.pack
                    new_emp = None
                fin.write(code_bytes)
                fin.write(name.encode("utf-8"))
                fin.write(b"\x00" * (20 - len(name)))
                fin.write(salary_bytes)

        print("Record inserted successfully.")
        os.remove("EMPLOYEE.DAT")
        os.rename("TEMP.DAT", "EMPLOYEE.DAT")
    except FileNotFoundError:
        print("EMPLOYEE.DAT file not found. Cannot insert record.")


if __name__ == "__main__":
    print("******************************************************************")
    print("            EMPLOYEE MANAGEMENT SYSTEM !!")
    print("******************************************************************")

    delete_existing_file()

    while True:
        print("ENTER CHOICE")
        print("1. ADD AN EMPLOYEE")
        print("2. DISPLAY")
        print("3. SEARCH")
        print("4. INCREASE SALARY")
        print("5. INSERT RECORD")
        try:
            n = int(input("Make a choice: "))

            if n == 1:
                append_to_file()
            elif n == 2:
                display_all()
            elif n == 3:
                search_for_record()
            elif n == 4:
                increase_salary()
            elif n == 5:
                insert_record()
            else:
                print("Invalid Choice")

            ch = input("Do you want to continue? (Y/N): ")
            if ch.lower() != 'y':
                break

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print("****************************************************************")
    print("                          THANKING YOU")
    print("****************************************************************")
