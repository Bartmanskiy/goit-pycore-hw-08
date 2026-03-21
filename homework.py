from collections import UserDict
from datetime import datetime, date, timedelta
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

class PhoneNotFoundError(Exception):
    pass

class InvalidPhoneError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
           raise ValueError("Please enter a phone with 10 numbers")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")	
        super().__init__(value)
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value: str):
          self.phones.append(Phone(value))
    
    def remove_phone(self, value: str):
        phone = self.find_phone(value)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone {value} not found in {self.name.value}'s record")
    
    def edit_phone(self, old_value: str, new_value: str):
        phone = self.find_phone(old_value)
        if not phone:
            raise ValueError(f"Phone {old_value} not found in {self.name.value}'s record")
        new_phone = Phone(new_value)
        phone.value = new_phone.value
    
    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = self.birthday.value if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {bday}"

class AddressBook(UserDict):
    def add_record(self, record):
         self.data[record.name.value] = record

    def find(self, name):
         return self.data.get(name)
    
    def delete(self, name):
         if name in self.data:
             del self.data[name]
    
    def get_upcoming_birthdays(self, days=7):
        today = date.today()
        upcoming = [] 
        for record in self.data.values():
            if not record.birthday:
                continue             
            bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            bday = bday.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if bday.weekday() == 5:
                bday += timedelta(days=2)
            elif bday.weekday() == 6:    # неділя
                bday += timedelta(days=1)
            if 0 <= (bday - today).days <= days:
                upcoming.append({"name": record.name.value, "birthday": bday.strftime("%d.%m.%Y")})
        return upcoming  

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Not enough arguments."
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def edit_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."

@input_error
def phone_username(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    phones = ", ".join([p.value for p in record.phones])
    return f"{name}: {phones}"

@input_error
def all_users(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    output = []
    for record in book.data.values():
        phones = ", ".join([p.value for p in record.phones]) if record.phones else "N/A"
        bday = record.birthday.value if record.birthday else "N/A"
        output.append(f"{record.name.value} | Phones: {phones} | Birthday: {bday}")
    return "\n".join(output)

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if not record:
       return 'Contact not found'
    record.add_birthday(birthday)
    return f'Birthday for {name} added'

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday:
        return "Birthday not set."
    return f"{name}'s birthday is {record.birthday.value}"

@input_error
def birthdays(args, book):
    try:
        days = int(args[0]) if args else 7
    except ValueError:
        return "Invalid number of days."
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(f"{item['name']} - {item['birthday']}" for item in upcoming)

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        
        if not user_input: 
            print("Please enter a command.")
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(edit_phone(args, book))

        elif command == "phone":
            print(phone_username(args, book))

        elif command == "all":
            print(all_users(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
    
    save_data(book)

if __name__ == "__main__":
    main()
