from collections import UserDict
from datetime import datetime, date, timedelta
import pickle

def save_data(book, filename="addressbook.txt"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.txt"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

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
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")	
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value: str):
          self.phones.append(Phone(value))
    
    def remove_phone(self, value: str):
        self.phones = [phone for phone in self.phones if phone.value != value]
    
    def change_phone(self, old_value: str, new_value: str):
        for phone in self.phones:
            if phone.value == old_value:
                phone.value = new_value
                return True
        return False
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

class AddressBook(UserDict):
    def add_record(self, record):
         self.data[record.name.value] = record

    def find(self, name):
         return self.data.get(name)
    
    def delete(self, name):
         if name in self.data:
             del self.data[name]
    
    def get_birthdays(self, days=7):
        today = date.today()
        upcoming = []
        for record in self.data.values():
            if not record.birthday:
                continue             
            bday = record.birthday.value.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if bday.weekday() == 5:
                bday += timedelta(days=2)
            elif bday.weekday() == 6:    # неділя
                bday += timedelta(days=1)
            if 0 <= (bday - today).days <= days:
                upcoming.append({"name": record.name.value, "bday": bday.strftime("%d.%m.%Y")})
        return upcoming

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Повертаємо текст помилки з виключення
            return f"Error: {e}"
        except IndexError:
            # Коли не вистачає аргументів
            return "Error: Not enough arguments."
        except KeyError:
            return "Error: Contact not found."
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
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    if record.change_phone(old_phone, new_phone):
        return "Phone updated."
    return "Old phone not found."

@input_error
def phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    phones = ", ".join([p.value for p in record.phones])
    return f"{name}: {phones}"

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    output = []
    for record in book.data.values():
        phones = ", ".join([p.value for p in record.phones]) if record.phones else "N/A"
        bday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "N/A"
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
    return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book):
    days = int(args[0]) if args else 7
    upcoming = book.get_birthdays(days)
    
    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(f"{item['name']} - {item['bday']}" for item in upcoming)

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays   
    }

    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")
                print("Commands: add, change, phone, all, add-birthday, show-birthday, birthdays, exit")
   
            elif command in commands:
                print(commands[command](args, book))
    
            else:
                print("Invalid command.")
    finally:
        save_data(book, "adressbook.txt")

if __name__ == "__main__":
    main()
