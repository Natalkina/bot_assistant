from Address_book.Application import AddressBookApplication
from Address_book.Models import AddressBook
from personal_assistant.ResponseWriter import ConsoleResponseWriter

application = AddressBookApplication(AddressBook('addressbook.csv'))
writer = ConsoleResponseWriter()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Sorry, reading from invalid index"
        except Exception as e:
            return str(e)
    return wrapper


def hello(*args):
    return """How can I help you?\n 
               You can choose one of the commands:\n 
               "add",\n                              
               "phone add" \n                  
               "phone change" \n            
               "phone remove"\n           
               "days to birthday"\n   
               "hello"\n                          
               "change"\n                       
               "phone"\n                         
               "show all"\n                    
               "search"\n                        
               "close"\n                         
               "good bye"\n                       
               "exit": close """


@input_error
def close(*args):
    answer = input(">>> Would you like to save changes (Y/N)? ")
    if answer == "N":
        exit(0)
    elif answer == "Y":
        application.save()
        writer.write("The changes has been saved to file addressbook.csv ")
        exit(0)
    else:
        raise Exception("Please enter Y or N")


def command_parser(COMMANDS, user_input: str):
    for key_word, command in COMMANDS.items():
        if user_input.lower().startswith(key_word):
            return command, user_input.replace(key_word, "").strip().split(" ")
    return None, None


def main():
    COMMANDS = {
        "add": application.add,
        "phone add": application.add_phone,
        "phone change": application.change_phone,
        "phone remove": application.remove_phone,
        "days to birthday": application.days_to_birthday,
        "hello": hello,
        "change": application.change,
        "phone": application.phone,
        "show all": application.show_all,
        "search": application.search,
        "close": close,
        "good bye": close,
        "exit": close,
    }

    while True:
        user_input = input(">>> ")
        command, data = command_parser(COMMANDS, user_input)

        if not command:
            writer.write("Sorry, unknown command")
        else:
            writer.write(command(*data))


if __name__ == '__main__':
    main()
