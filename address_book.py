from collections import UserDict
from datetime import datetime, timedelta

PHONE_LENGTH = 10

class Validator:
    def not_empty(self, value, error_message):
        if len(value.strip()) == 0:
            raise ValueError(error_message)

    def len(self, value, expected_len, error_message):
        if not isinstance(value, str):
            raise ValueError(error_message)
        if len(value) is not expected_len:
            raise ValueError(error_message)

    def date(self, value, format, error_message):
        if not isinstance(value, str):
            raise ValueError(error_message)

        # parsing wrong string will raise an error if format is not suitable.
        try:
            return datetime.strptime(value, format).date()
        except:
            raise ValueError(f"Incorrect birthday format. Use `{format}`")

    def only_numbers(self, value, error_message):
        return

class Field:
    validator = Validator()
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        self.validate(name)
        super().__init__(name)

    def set_name(self, new_name):
        self.validate(new_name)
        self.value = new_name

    def validate(self, value):
        self.validator.not_empty(value, "Name should not be empty")


class Phone(Field):
    def __init__(self, phone):
        self.validate(str(phone))
        super().__init__(str(phone))

    def set_value(self, value):
        self.validate(value)
        self.value = value

    def validate(self, value):
        self.validator.not_empty(value, "Phone should not be empty")
        self.validator.len(value, PHONE_LENGTH, f"Phone should have {PHONE_LENGTH} numbers")


class Birthday(Field):
    format = "%d.%m.%Y"
    expected_format = "DD.MM.YYYY"
    def __init__(self, value):
        valid_value = self.validator.date(
            value,
            self.format,
            f"Invalid date format. Use {self.expected_format}"
        )
        super().__init__(valid_value)

    def __str__(self):
        return str(self.value.strftime(self.format))

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        found_phone.set_value(new_phone)

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        self.phones.remove(found_phone)

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i

        raise ValueError(f"Phone `{phone}` not found")

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __str__(self):
        return f"Contact Name={self.name.value}, Phones={'; '.join(p.value for p in self.phones)}, Birthday={self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name, silent = False):
        if name in self.data:
            return self.data[name]

        if silent:
            return None

        raise ValueError(f'Contact `{name}` not found.')

    def delete(self, name):
        found_record = self.find(name)
        if found_record:
            self.data.pop(name)

    def get_upcoming_birthdays(self):
        upcoming = []
        today = datetime.today().date()

        for key in self.data:
            record = self.data[key]
            print(record)
            # Birthday for this year (or next year if already passed)
            birth = record.birthday.value.replace(year=today.year)

            if birth < today:
                birth = birth.replace(year=today.year + 1)

            delta_days = (birth - today).days

            # Check if birthday is within the next 7 days
            if 0 <= delta_days <= 6:
                congratulation = birth

                # Move to Monday if birthday falls on weekend
                if congratulation.weekday() == 5:
                    congratulation += timedelta(days=2)
                if congratulation.weekday() == 6:
                    congratulation += timedelta(days=1)

                upcoming.append({
                    'user': key,
                    'congratulation_date': birth.strftime("%d.%m.%Y"),
                })

        return upcoming
