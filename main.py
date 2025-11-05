import pickle

from address_book import Record
from store import load_data, save_data


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def safe_args(count: int, *args) -> list:
    arguments = list(*args)
    result = []
    for i in range(count):
        result.append(arguments[i] if len(arguments) > i else None)
    return result


def welcome_message():
    return "Welcome to the assistant bot!\nAddress Book 1.0.\nEnter 'help' to see all supported commands."

def command_handler_exit(book, args):
    return "Good bye!"

def command_handler_hello(*args):
    return "How can I help you?"

def command_handler_help(*args):
    return f"""
Command list:
{'help':>15} - Show this help
{'add':>15} - Add new contact. Example: add username +0981112233 birthday
{'change':>15} - Change contact phone. Example: change username +0982223344
{'phone':>15} - Show phone by contact. Example: phone username
{'all':>15} - Show all contacts
{'add-birthday':>15} - Add birthday. Example: add-birthday username 24.04.1999
{'show-birthday':>15} - Show user's birthday. Example: show-birthday username
{'birthdays':>15} - Show birthdays of all users.
{'exit':>15} - Exit the program.
{'close':>15} - Close the program.
{'hello':>15} - Welcome message.
"""

def command_handler_add(book, *args):
    name, phone, birthday = safe_args(3, *args)
    record = book.find(name, silent=True)

    if not record:
        record = Record(name)
    if phone:
        record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    book.add_record(record)
    return "Record added."

def command_handler_change(book, *args):
    name, old_phone, new_phone = safe_args(3, *args)
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return 'Contact changed.'

def command_handler_phone(book, *args):
    name, phone = safe_args(2, *args)
    record = book.find(name)
    return ', '.join(str(p) for p in record.phones)

def command_handler_all(book, *args):
    result = []
    for key in book:
        value = book[key]
        result.append(str(value))
    return '\n'.join(result)

def command_handler_add_birthday(book, *args):
    name, birthday = safe_args(2, *args)
    found_record = book.find(name)
    found_record.add_birthday(birthday)
    book.notify('change')
    return "Birthday added."

def command_handler_show_birthday(book, *args):
    name, phone = safe_args(2, *args)
    record = book.find(name)
    return record.birthday

def command_handler_birthdays(book, *args):
    return book.get_upcoming_birthdays()

commands = {
    'exit': command_handler_exit,
    'close': command_handler_exit,
    'hello': command_handler_hello,
    'help': command_handler_help,
    'add': command_handler_add,
    'change': command_handler_change,
    'phone': command_handler_phone,
    'all': command_handler_all,
    'add-birthday': command_handler_add_birthday,
    'show-birthday': command_handler_show_birthday,
    'birthdays': command_handler_birthdays,
}

def main():
    book = load_data()
    print(welcome_message())

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in commands:
            try:
                print(commands[command](book, *args))
                if command in ['exit', 'close']:
                    break
            except Exception as error:
                print(error)
        else:
            print(f"Invalid command. Type 'help' to see all supported commands.")

    save_data(book)

if __name__ == '__main__':
    main()