from collections import UserDict, defaultdict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone_number):
        if len(phone_number) == 10 and phone_number.isdigit():
            super().__init__(phone_number)
        else:
            raise ValueError("Phone number must contain 10 digits.")


class Birthday(Field):
    def __init__(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
        except ValueError as e:
            print(e)

    def remove_phone(self, phone_number):
        self.phones = [
            phone for phone in self.phones if phone.value != phone_number
        ]

    def edit_phone(self, phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                try:
                    phone.value = new_phone_number
                except ValueError as e:
                    print(f"Failed to edit phone: {e}")
                return

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(f"Impossible to add birthday. {e}")

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {phones_str}, " \
                f"birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]


def get_birthdays_per_week(self):
    birthday_on_week = defaultdict(list)
    today = datetime.today().date()
    one_week_from_today = today + timedelta(days=7)

    for record in self.data.values():
        if record.birthday:
            birthday_date = datetime.strptime(
                record.birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)

            if today <= birthday_this_year <= one_week_from_today:
                if birthday_this_year.strftime("%A") in ["Saturday", "Sunday"]:
                    day_name = "Monday"
                else:
                    day_name = birthday_this_year.strftime("%A")
                birthday_on_week[day_name].append(record.name.value)

    birthday_on_week = dict(birthday_on_week)
    for day, employees in birthday_on_week.items():
        if employees:
            employees_str = ", ".join(employees)
            print(f"{day}: {employees_str}")
    if not birthday_on_week:
        print("No birthdays in the next week.")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"Contact {e} not found."
        except IndexError:
            return "The index you entered is out of range."
    return inner


@input_error
def add_contact(book, args):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name = args[0]
    phone = args[1]

    record = book.find(name)
    if record:
        record.add_phone(phone)
        print(f"Phone number added for contact {name}.")
    else:
        record = Record(name)
        try:
            Phone(phone)
        except ValueError as e:
            print(e)
            return
        record.add_phone(phone)
        book.add_record(record)
        print("Contact added.")


@input_error
def change_contact(book, name, new_phone):
    record = book.find(name)
    if record:
        if record.phones:
            current_phone = record.phones[0].value
            record.edit_phone(current_phone, new_phone)
            print("Contact updated.")
        else:
            print(f"No phone number found for {name}.")
    else:
        print(f"Contact {name} not found.")


@input_error
def delete_contact(self, name):
    if name in self.data:
        del self.data[name]
        print(f"Contact {name} deleted.")
    else:
        print(f"Contact {name} not found.")


@input_error
def show_phone(book, name):
    record = book.find(name)
    if record:
        if record.phones:
            print(record.phones[0])
        else:
            print(f"No phone number found for {name}.")
    else:
        print(f"Contact {name} not found.")


@input_error
def show_all(book):
    if not book.data:
        print("The contact list is empty")
    else:
        for record in book.data.values():
            print(record)


@input_error
def add_birthday(book, name, birthday):
    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday)
            return "Birthday added."
        except ValueError as e:
            print(f"Impossible to add birthday. {e}")
    else:
        print(f"Contact {name} not found.")


@input_error
def show_birthday(book, args):
    if args:
        name = args[0]
        record = book.find(name)
        if record:
            if record.birthday:
                print(f"Birthday for {name}: {record.birthday}")
            else:
                print(f"No birthday found for {name}.")
        else:
            print(f"Contact {name} not found.")
    else:
        print("Please provide a name.")


def main():
    book = AddressBook()
    print("Welcome to the assistant bot! \nType 'menu' to see commands.")

    menu = """
    Available Commands:
    - hello: > Print a welcome message.
    - add [name] [phone]: > Add a new contact with a name and phone number.
    - change [name] [new_phone]: > Change phone number for an existing contact.
    - phone [name]: > Show the phone number for a contact.
    - all: Show all contacts.
    - add-birthday [name] [birthday]: > Add a birthday (DD.MM.YYYY) for a contact.
    - show-birthday [name]: > Show the birthday for a contact.
    - birthdays: > Show birthdays in the next week.
    - delete [name]: > Delete a contact.
    - menu: > Show the available commands and their explanations.
    - close or exit: > Exit the program.
    """

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "menu":
            print(menu)
        elif command == "add":
            if len(args) < 2:
                print("Give me name and phone please.")
            else:
                add_contact(book, args)
        elif command == "change":
            if len(args) < 2:
                print("Give me name and phone please.")
            else:
                name, phone = args
                change_contact(book, name, phone)
        elif command == "phone":
            if len(args) < 1:
                print("Please provide a name.")
            else:
                name = args[0]
                show_phone(book, name)
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            if len(args) < 2:
                print("Give me name and birthday please.")
            else:
                name, birthday = args
                result = add_birthday(book, name, birthday)
                print(result)
        elif command == "show-birthday":
            show_birthday(book, args)
        elif command == "birthdays":
            get_birthdays_per_week(book)
        elif command == "delete":
            if len(args) < 1:
                print("Please provide a name.")
            else:
                name = args[0]
                delete_contact(book, name)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
