from abc import ABC, abstractmethod
from collections import UserDict
import csv
from datetime import date, datetime
import re
import os


class AbstractField(ABC):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.assert_valid_value(value)
        self._value = value

    @abstractmethod
    def assert_valid_value(self, value):
        pass


class Name(AbstractField):

    def assert_valid_value(self, value):
        if not value.isalpha():
            raise Exception("Please enter correct name")


class Phone(AbstractField):
    def assert_valid_value(self, value):
        if not value.isnumeric():
            raise Exception("Please enter correct phone number")


class Birthday(AbstractField):

    @classmethod
    def fromisoformat(cls, value):
        if not datetime.strptime(value, "%Y-%m-%d"):
            raise Exception("Please enter date number as 'YYYY-MM-DD'")
        return cls(date.fromisoformat(value))

    def assert_valid_value(self, value):
        if not isinstance(value, date):
            raise Exception("Please enter number as 'YYYY-MM-DD'")

    def days_diff(self, date):

        delta1 = datetime(date.year, self.value.month, self.value.day)
        delta2 = datetime(date.year + 1, self.value.month, self.value.day)
        if delta1 > date:
            return (delta1 - date).days
        else:
            return (delta2 - date).days

    def __str__(self):
        return self.value.strftime("%Y-%m-%d")


class Email(AbstractField):
    def assert_valid_value(self, value):
        if not re.search(r"[a-zA-Z]\w*[.]?\w*[.]?\w*'@'\w+[.]\w{2}\w*", self.value):
            raise Exception("Please enter correct email")


class Address(AbstractField):
    def assert_valid_value(self, value):
        if len(self.value) >= 256:
            raise Exception("Please enter your address not so large")

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, address: Address = None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_phone(self, add_phone: Phone):
        self.phones.append(add_phone)

    def remove_phone(self, removable_phone: Phone):
        self.phones = [n for n in self.phones if n != removable_phone]

    def change_phone(self, changeable_phone: Phone, new_phone: Phone):

        for i, n in enumerate(self.phones):
            if n == changeable_phone:
                self.phones[i] = new_phone
        return self.phones

    def add_phones(self, phones: list[Phone]):
        self.phones += phones
        return self

    def __str__(self):
        return self.name.value + repr(self.phones) + repr(self.birthday) + repr(self.email) + repr(self.address)

    def __repr__(self):
        return str(self)


class AddressBook(UserDict[str, Record]):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.load_from_csv()

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def change_record(self, record: Record) -> object:
        if record.name.value in self.data:
            self.data[record.name.value] = record
        else:
            raise Exception(f"This name {record.name.value} is not found. Please input correct name")

    def iterator(self, page_size: int) -> list[Record]:
        page = [None] * page_size
        idx = 0
        for record in self.data.values():
            page[idx] = record
            idx += 1
            if idx == page_size:
                yield page
                idx = 0
        yield page[:idx]

    def search(self, term: str):
        for record in self.data.values():
            if term in record.name.value:
                yield record
            else:
                for phone in record.phones:
                    if term in str(phone):
                        yield record
                        break

    def write_to_csv(self,):
        with open(self.filename, 'w', encoding='UTF8', newline='') as file:
            fieldnames = ["Name", "Phones", "Birthday", "Email", "Address"]
            writer = csv.DictWriter(
                file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.data.values():
                writer.writerow({
                    "Name": record.name,
                    "Phones": record.phones,
                    "Birthday": record.birthday,
                    "Email": record.email,
                    "Address": record.address
                })

    def load_from_csv(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                name = row["Name"]
                birthday = row["Birthday"]
                email = row["Email"]
                address = row["Address"]
                phones = [Phone(p) for p in row["Phones"][1:-1].split(", ")]
                self.data[name] = Record(
                    Name(name),
                    None,
                    Birthday.fromisoformat(birthday) if birthday else None,
                    Email(email) if email else None,
                    Address(address) if address else None
                ).add_phones(phones)

