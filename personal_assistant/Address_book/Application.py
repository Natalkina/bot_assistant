from datetime import datetime
from Models import AddressBook, Address, Birthday, Email, Name, Phone, Record


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Sorry, reading from invalid index"
        except Exception as e:
            return str(e)

    return wrapper


class AddressBookApplication:
    def __init__(self, contacts: AddressBook):
        self.contacts = contacts

    @input_error
    def save(self):
        self.contacts.write_to_csv()

    @input_error
    def add(self, *args):
        name = args[0]
        phone_number = args[1]
        birthday = Birthday.fromisoformat(args[2]) if len(args) >= 3 else None
        email = Email(args[3]) if len(args) >= 4 else None
        address = Address(args[4]) if len(args) >= 5 else None
        self.contacts.add_record(
            Record(
                Name(name),
                Phone(phone_number),
                birthday,
                email,
                address
            )
        )

        message = f"This is ADD, name {name}, phone {phone_number}"
        if birthday and email and address:
            message += f", birthday {birthday}, email {email}, address {address}"
        elif birthday:
            message += f", and birthday {birthday.value}"
        return message

    @input_error
    def add_phone(self, *args):
        name = args[0]
        phone_number = args[1]
        if name in self.contacts.keys():
            self.contacts[name].add_phone(Phone(phone_number))
            return f"This is ADD, name {name}, phone {phone_number}"
        else:
            return f"This Name {name} is not found in contacts"

    @input_error
    def remove_phone(self, *args):
        name = args[0]
        phone_number = args[1]
        if name in self.contacts.keys():
            if Phone(phone_number) in self.contacts[name].phones:
                self.contacts[name].remove_phone(Phone(phone_number))
                return f"This is REMOVE phone {phone_number} from name {name}"
            else:
                return f"This {phone_number} is not defined"
        else:
            return f"This Name {name} is not found in contacts"

    @input_error
    def change_phone(self, *args):
        name = args[0]
        phone_number = args[1]
        new_phone_number = args[2]
        if name in self.contacts.keys():
            if Phone(phone_number) in self.contacts[name].phones:
                self.contacts[name].change_phone(Phone(phone_number), Phone(new_phone_number))
                return f"This is CHANGE phone {phone_number} to new number {new_phone_number} for name {name}"
            else:
                return f"This phone number {phone_number} is not defined"
        else:
            return f"This Name {name} is not found in contacts"

    @input_error
    def change(self, *args):
        name = args[0]
        phone_number = args[1]
        if name in self.contacts.keys():
            self.contacts.change_record(
                Record(
                    Name(name),
                    [Phone(phone_number)]
                )
            )
            return f"This is CHANGE, phone {phone_number} for name {name}"
        else:
            raise Exception("Name is not found in contacts")

    @input_error
    def phone(self, *args):
        name = args[0]
        if name in self.contacts.keys():
            return f"This is phone {self.contacts.get(name).phones} for name {name}"

        else:
            raise Exception("Name is not found in contacts")

    @input_error
    def days_to_birthday(self, *args):
        name = args[0]
        if name in self.contacts.keys():
            record = self.contacts[name]
            if record.birthday:
                days = record.birthday.days_diff(datetime.now())

                return f"The {days} days left to birthday of contact {name}"

            else:
                raise Exception(f"This contact {name} has no information about birthday")
        else:
            raise Exception("Please input correct name")

    @input_error
    def search(self, *args):
        term = args[0]
        pattern = '{0:10} {1:10} {2:10} {3:10} {4:10}\n'
        table = pattern.format("Name", "Phones", "Birthday")
        for record in self.contacts.search(term):
            table += pattern.format(
                record.name.value,
                ", ".join(map(repr, record.phones)),
                str(record.birthday.value) if record.birthday else "None",
                str(record.email.value) if record.email else "None",
                str(record.address.value) if record.address else "None"
            )

        return table

    @input_error
    def show_all(self, *args):
        pattern = '{0:10} {1:10} {2:10} {3:10} {4:10}\n'
        table = pattern.format("Name", "Phones", "Birthday", "Email", "Address")
        for page in self.contacts.iterator(5):
            for record in page:
                table += pattern.format(
                    record.name.value,
                    ", ".join(map(repr, record.phones)),
                    str(record.birthday.value) if record.birthday else "None",
                    str(record.email.value) if record.email else "None",
                    str(record.address.value) if record.address else "None"
                )
        return table
