from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime, timedelta
import csv
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
import time

finish_words = ["goodbye", "close", "exit"]
COMMAND_WORDS = ["add", "change", "show_phone", "show_all", "help", "delete", "address", "email", "birthday", "days_to_birthday", "get_birthdays", "save", "show_address", "show_email", "show_birthday", "get_book", "find"]
Autocomplete_words = ["goodbye", "close", "exit", "add", "change", "phone", "show_all", "help", "delete", "address", "email", "birthday", "days_to_birthday", "get_birthdays", "save", "get_book", "find"]

class PhoneNotInt(Exception):
    pass

class BirthdayNotDate(Exception):
    pass

class EmailNotEmail(Exception):
    pass


class AddressBook(UserDict):

    user_id = 0
            
    def __iter__(self):
        return Iterable(len(self.data), self.quantity_on_page)

    
    def add_record(self, new_user):

        AddressBook.user_id += 1
        
        if type(new_user) == str:
            return new_user

        for key, val in new_user.items():
            self.data[key] = val
            return {key: val}

    def get_contacts(self):
        return self.data
    

    def get_contacts_pages(self, quantity_on_page):
        self.contacts_on_page = []
        self.dict_on_page = {}
        len_add_book = len(self.data)
        i = -1
        for key, val in self.data.items():
            
  
            self.dict_on_page.update({key: val})
            
            if len(self.dict_on_page) >= quantity_on_page:
                self.contacts_on_page.append(self.dict_on_page)
                self.dict_on_page = {}
        if self.dict_on_page:
            self.contacts_on_page.append(self.dict_on_page)
        return self.contacts_on_page

    def saving_address_book(self):

        with open("address_book.csv", "w", newline = "") as fh:
            field_names = ["name", "phones", "birthday", "email", "address"]
            writer = csv.DictWriter(fh, fieldnames = field_names)
            writer.writeheader()
            for val in self.data.values():
                writer.writerow(val)

    def unpaking_address_book(self):

        with open("address_book.csv", "r", newline = "") as fh:
            self.unpacked_data = {}
            reader = csv.DictReader(fh)
            for row in reader:
                users_phones_list = []
                phones_with_pref_suf = row["phones"][2:len(row["phones"])-2:]
                users_phones_list_base = phones_with_pref_suf.split("', '")
                for element in users_phones_list_base:
                    users_phones_list.append(str(element))
                self.unpacked_data[row["name"]] = {"name": row["name"], "phones": users_phones_list, "birthday": row["birthday"], "email": row["email"], "address": row["address"]}

            if not self.data:
                self.data = self.unpacked_data
            else:
                for key, val in self.unpacked_data.items():
                    if key in self.data:
                        continue
                    else:
                        self.data[key] = val

        return self.data

    def find_contact(self, part_of_data):
        self.found_list = []
        for key, val in self.data.items():

            for phone in self.data[key]["phones"]:
                if part_of_data in phone and not {key: val} in self.found_list:
                    self.found_list.append({key: val})

            for cont_data in val.values():
                if cont_data != None and part_of_data in cont_data:
                    self.found_list.append({key: val})
        if not self.found_list:
            return f"There is no contacts with this data"
        else:
            return self.found_list

class Iterable():

    def __init__(self, len_address_book, quantity_on_page):
        self.len_address_book = len_address_book
        self.quantity_on_page = quantity_on_page
        self.current_contacts = -1
        self.page_number = -1

    def __next__(self):
        if self.current_contacts <= self.len_address_book:
            self.page_number += 1
            self.current_contacts += self.quantity_on_page
            return AddressBook().contacts_on_page[self.page_number]
        else:
            if self.len_address_book//self.quantity_on_page:
                self.page_number += 1
                return AddressBook().contacts_on_page[self.page_number]
        raise StopIteration

class AbstractGuide(ABC):

    @abstractmethod
    def show_info(self):
        pass

class Guide(AbstractGuide):

    def show_info(self):
        return """Enter\n
                          'add' and user's name and phone to add the user,\n
                          'birthday' and user's name and birthday in format DD.MM.YYYY to add the birthday,\n
                          'days_to_birthday' to see the quantity of days till user's birthday,\n
                          'get_birthdays' and number for seaching users with birthdays in number days,\n
                          'change' and user's name and phone for changing the phone number,\n
                          'show_phone' and user's name to show the phone number,\n
                          'show_email' and user's name to show the email,\n
                          'show_address' and user's name to show the address,\n
                          'show_birthday' and user's name to show the birthday,\n
                          'show_all' and quantity of users on page to see all users,\n
                          'email' and user's name and email to add the email,\n
                          'address' and user's name and address to add the address,\n
                          'delete' and user's name to delete the contact,\n
                          'save' for saving the address book to 'address_book.csv' in curerent folder,\n
                          'get_book' to get the address book from 'address_book.csv' in curerent folder,\n
                          'find' and part of data that you want to find to find the contacts with this data"""



class AbstactUserInfo(ABC):
    
    @abstractmethod
    def info_about_user(self, name, address_book):
        pass

class UserPhone(AbstactUserInfo):

    def info_about_user(self, name, address_book):
        
        for key, val in address_book.items():
            if key == name:
                return f"the user {key} has the next phone numbers {address_book[key]['phones']}"
        return f"There is not {name} in the Address book"

class UserBirthday(AbstactUserInfo):

    def info_about_user(self, name, address_book):

        for key, val in address_book.items():
            if key == name:
                return f"the user {key} has birthday {address_book[key]['birthday']}"
        return f"There is not {name} in the Address book"
        

class UserAddress(AbstactUserInfo):

    def info_about_user(self, name, address_book):

        for key, val in address_book.items():
            if key == name:
                return f"the user {key} has the next address {address_book[key]['address']}"
        return f"There is not {name} in the Address book"

class UserEmail(AbstactUserInfo):

    def info_about_user(self, name, address_book):

        for key, val in address_book.items():
            if key == name:
                return f"the user {key} has the next email {address_book[key]['email']}"
        return f"There is not {name} in the Address book"  



class Field:
    pass

    
    

class Record(Field):

    def record_name(self, name):
        self.name = name
        return self.name


    def record_phone(self, phones):
        self.phone_numb = phones
        return self.phone_numb

    def record_birth(self, birthday):
        self.birthday_date = birthday
        return self.birthday_date

    def add_user(self, name, phones, address_book, birthday = None, email = None, address = None):

        new_user = {}

        if len(address_book):

            for elem in address_book:
                if name == elem:
                    name = name + str(AddressBook.user_id)

        new_user[name] = {"name": name, "phones": phones, "birthday": birthday, "email": email, "address": address}

        return new_user

    def change_number(self, name, phones, address_book):
        for key, val in address_book.items():
            if key == name:
                return {name: {"name": name, "phones": phones, "birthday": address_book[key]["birthday"], "email": address_book[key]["email"], "address": address_book[key]["address"]}}
        return f"There is no user with name {name}"

    def add_address(self, name, address, address_book):
        for key, val in address_book.items():
            if key == name:
                return {name: {"name": name, "phones": address_book[key]["phones"], "birthday": address_book[key]["birthday"], "email": address_book[key]["email"], "address": address}}
        return f"There is no user with name {name}"

    def add_birthday(self, name, birthday, address_book):
        for key, val in address_book.items():
            if key == name:
                return {name: {"name": name, "phones": address_book[key]["phones"], "birthday": birthday, "email": address_book[key]["email"], "address": address_book[key]["address"]}}
        return f"There is no user with name {name}"

    def add_email(self, name, email, address_book):
        for key, val in address_book.items():
            if key == name:
                return {name: {"name": name, "phones": address_book[key]["phones"], "birthday": address_book[key]["birthday"], "email": email, "address": address_book[key]["address"]}}
        return f"There is no user with name {name}"

    def show_phone(self, name, address_book):

        for key, val in address_book.items():
            if key == name:
                return f"the user {key} has the next phone numbers {address_book[key]['phones']}"
        return f"There is not {name} in the Address book"

    def days_to_birthday(self, name, address_book):
        for key, val in address_book.items():
            if key == name and address_book[key]["birthday"]:
                self.date_today = datetime.now()
                self.next_birthday = datetime(year = self.date_today.year, month = int(address_book[key]["birthday"][3:5]), day = int(address_book[key]["birthday"][0:2]))
                if self.next_birthday - self.date_today < timedelta(days=0):
                    self.next_birthday = datetime(year = self.date_today.year+1, month = int(address_book[key]["birthday"][3:5]), day = int(address_book[key]["birthday"][0:2]))
                    difference = str(self.next_birthday-self.date_today).split(",")
                    days_till_birthday = difference[0].split(" ")
                    return days_till_birthday[0]
                elif self.next_birthday - self.date_today >= timedelta(days=0):
                    difference = str(self.next_birthday-self.date_today).split(",")
                    days_till_birthday = difference[0].split(" ")
                    return days_till_birthday[0]
        return f"There is not {name} in the Address book or user doesn't save the birthday"


class Name(Field):

    def user_name_def(self, name):
        self.name_value = name
        return self.name_value

class Address(Field):

    def address(self, address):
        self.address = address
        return self.address

class Email(Field):

    def __init__(self):
        self.__email = ""

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):

        self.__email = new_email
        check_email = re.search(r"[a-zA-Z]\w\w*[.]?\w*[.]?\w*[@]\w+[.]\w{2}\w*", self.__email)


        while True:

            try:

                if not check_email:
                    raise EmailNotEmail

            except EmailNotEmail:
                self.__email = input("Please, enter the actual email in format xx@xx.xx ")
                check_email = re.search(r"[a-zA-Z]\w\w*[.]?\w*[.]?\w*[@]\w+[.]\w{2}\w*", self.__email)
            else:
                break

        return self.__email

class Phone(Field):

    def __init__(self):
        self.__phones = []


    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def phones(self, new_phone):

        self.__phones = new_phone
        i = 0

        while i < len(self.__phones):

            try:
                for elem in self.__phones:
                    check_phone = re.search(r"[+]\d{10}", elem)
                    if not check_phone:
                        raise PhoneNotInt
                    else:
                        i += 1
            except PhoneNotInt:
                    inp_phones = input("Phones should be in format +XXXXXXXXXXXX. Please, enter in this format: ")
                    self.__phones = inp_phones.split(" ")
                    i=0

            else:
                return self.__phones

class Birthday(Field):

    def __init__(self):
        self.__birthday = ""

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, new_birthday):

        self.__birthday = new_birthday
        self.current_day = datetime.now()
        birth_date = self.__birthday.split(".")

        while True:

            try:

                for elem in birth_date:
                    if not elem.isdigit():
                        raise BirthdayNotDate
                if len(birth_date) != 3:
                    raise BirthdayNotDate
                if int(birth_date[1]) > 12 or int(birth_date[1]) < 1 or int(birth_date[0]) < 1:
                    raise BirthdayNotDate
                if int(birth_date[2]) >= int(self.current_day.year) and int(birth_date[1]) > int(self.current_day.month) and int(birth_date[0]) > int(self.current_day.day):
                    raise BirthdayNotDate
                if int(birth_date[2]) > int(self.current_day.year) or int(birth_date[2]) < int(self.current_day.year)-100:
                    raise BirthdayNotDate
                if int(birth_date[1]) == 2:
                    if int(birth_date[2]) % 4 == 0 and int(birth_date[0]) > 29 or int(birth_date[2]) % 4 != 0 and int(birth_date[0]) > 28:
                        raise BirthdayNotDate
                if int(birth_date[1]) in [1, 3, 5, 7, 8, 10, 12]:
                    if int(birth_date[0]) > 31:
                        raise BirthdayNotDate
                    else:
                        break
                if int(birth_date[1]) in [4, 6, 9, 11]:
                    if int(birth_date[0]) > 30:
                        raise BirthdayNotDate
                    else:
                        break

            except BirthdayNotDate:
                self.__birthday = input("Please, enter the actual birthday in format DD.MM.YYYY ")
                birth_date = self.__birthday.split(".")
            else:
                break

        return self.__birthday

command_completer = WordCompleter(Autocomplete_words,ignore_case=True,)


kb = KeyBindings()


@kb.add("c-space")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)



def main():

    """
    This function takes the command from user and do what the user asks.
    It stops the process when the key words are entered
    """

    contacts = AddressBook()

    first_command = input("Do you want to restore your saved address book? Enter Yes or No: ")
    first_command_small_letters = first_command.lower()

    if first_command_small_letters == "yes":

        try:
            contacts.unpaking_address_book()
        except FileNotFoundError:
            print("You don't have the saved address book")


    while True:

        change_user = Record()
        user_phone = Phone()
        user_birthday = Birthday()
        user_address = Address()
        user_email = Email()



               

        user_command = prompt(
            "Enter your command and data or enter 'help' to get the manual of bot  ",
            completer=command_completer,
            complete_while_typing=False,
            key_bindings=kb,
        ) 
        user_command_small_letters = user_command.lower()

        if user_command_small_letters == "hello":
            print("How can I help you?")




        for word in COMMAND_WORDS:

            user_data_small = user_command_small_letters.split(" ")

            if user_data_small[0] == word:

                user_data = user_command.split(" ")


                if user_data[0].lower() == "add":
                    if len(user_data) > 2:
                        user_phone.phones = user_data[2::]
                        print(f"add to the address book {contacts.add_record(change_user.add_user(change_user.record_name(Name().user_name_def(user_data[1])), change_user.record_phone(user_phone.phones), contacts.get_contacts()))}")

                elif user_data[0].lower() == "help":
                    print(Guide().show_info())
                    
                elif user_command_small_letters.startswith("show_all"):
                    if len(user_data) == 2:
                        pages = contacts.get_contacts_pages(int(user_data[1]))
                        if len(contacts.get_contacts())%int(user_data[1]):
                            for i in range(len(contacts.get_contacts())//int(user_data[1]) + 1):
                                print(f"page {i} {pages[i]}")
                        else:
                            for i in range(len(contacts.get_contacts())//int(user_data[1])):
                                print(f"page {i} {pages[i]}")

                elif user_data[0].lower() == "change":
                    if len(user_data) > 2:
                        user_phone.phones = user_data[2:]
                        contacts.add_record(change_user.change_number(change_user.record_name(Name().user_name_def(user_data[1])), change_user.record_phone(user_phone.phones), contacts.get_contacts()))
                        print(f"changes in the address book: for {change_user.record_name(Name().user_name_def(user_data[1]))} result {user_phone.phones}")

                elif user_data[0].lower() == "birthday":
                    if len(user_data) == 3:
                        user_birthday.birthday = user_data[2]
                        print(contacts.add_record(change_user.add_birthday(change_user.record_name(Name().user_name_def(user_data[1])), user_birthday.birthday, contacts.get_contacts())))

                elif user_data[0].lower() == "address":
                    if len(user_data) >= 3:
                        user_address.address = "".join(user_data[2:])
                        print(contacts.add_record(change_user.add_address(change_user.record_name(Name().user_name_def(user_data[1])), user_address.address, contacts.get_contacts())))


                elif user_data[0].lower() == "email":
                    if len(user_data) == 3:
                        user_email.email = user_data[2]
                        print(contacts.add_record(change_user.add_email(change_user.record_name(Name().user_name_def(user_data[1])), user_email.email, contacts.get_contacts())))

                elif user_data[0].lower() == "delete":
                    if len(user_data) == 2:
                        try:
                            contacts.get_contacts().pop(user_data[1])
                        except KeyError:
                            print(f"There is no {user_data[1]}in address book")
                        else:
                            print(f"{user_data[1]} was deleted from address book")
                            
                elif user_data[0].lower() == "show_phone":
                    if len(user_data) > 1:
                        print(UserPhone().info_about_user(Name().user_name_def(user_data[1]), contacts.get_contacts()))


                elif user_data[0].lower() == "show_address":
                    if len(user_data) > 1:
                        print(UserAddress().info_about_user(Name().user_name_def(user_data[1]), contacts.get_contacts()))

                elif user_data[0].lower() == "show_email":
                    if len(user_data) > 1:
                        print(UserEmail().info_about_user(Name().user_name_def(user_data[1]), contacts.get_contacts()))

                elif user_data[0].lower() == "show_birthday":
                    if len(user_data) > 1:
                        print(UserBirthday().info_about_user(Name().user_name_def(user_data[1]), contacts.get_contacts()))


                elif user_data[0].lower() == "days_to_birthday":
                    if len(user_data) > 1:
                        print(change_user.days_to_birthday(Name().user_name_def(user_data[1]), contacts.get_contacts()))

                elif user_data[0].lower() == "get_birthdays":
                    if len(user_data) == 2:
                        list_users_with_birthday = []

                        try:
                            if 0<=int(user_data[1])<366:
                                for key, val in contacts.get_contacts().items():
                                    if int(change_user.days_to_birthday(Name().user_name_def(key), contacts.get_contacts())) < int(user_data[1]):
                                        list_users_with_birthday.append({key: val})
                                print(list_users_with_birthday)
                        except ValueError:
                            print(f"The number of days till birthday should be as integer")

                    else:
                        print("Enter get_birthdays and number no more than 365")


                elif user_data[0].lower() == "save":
                    contacts.saving_address_book()

                elif user_data[0].lower() == "get_book":
                    try:
                        contacts.unpaking_address_book()
                    except FileNotFoundError:
                        print("You don't have the saved address book")

                elif user_data[0].lower() == "find":
                    if len(user_data) == 2:
                        print(contacts.find_contact(user_data[1]))

        if user_command_small_letters in finish_words:
            save_or_not = prompt(
            "Do you want to save? Enter Yes or No: ",
            completer=command_completer,
            complete_while_typing=False,
            key_bindings=kb,
            ) 
            save_or_not_small_letters = save_or_not.lower()
            if save_or_not_small_letters == "yes":
                contacts.saving_address_book()
                break
            break

    print("Good bye!")
    time.sleep(2)


if __name__ == '__main__':
    main()
