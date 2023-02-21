# Import the necessary packages
import Python_core_Team_3
import Clean_folder
import Notes
from consolemenu import *
from consolemenu.items import *
from termcolor import colored


def main_menu():


      a_b = "Address Book - the application that allows you to create and edit contacts.\nSee the application's Help for " \
            "details."
      n = "Notes- the application that allows you to create and edit notes.\nSee the application's Help for details."
      c_f = "Clean Folder - the application that sorts files in the specified folder.\nIn the input field, you have to " \
            "enter the path to the folder in which the files will be sorted"


      # Create the menu
      menu = ConsoleMenu(colored("CLI Assistant", "blue"),  colored("The application that provides work with the "
                                                                        "address book and notes, and also sorts files in "
                                                                        "the specified folder", "blue"))


      # A FunctionItem runs a Python function when selected
      address_book = FunctionItem(colored("Address Book", "yellow"), Python_core_Team_3.main, [])
      clean_folder = FunctionItem(colored("Clean Folder", "yellow"), Clean_folder.main, [])
      notes = FunctionItem(colored("Notes", "yellow"), Notes.main, [])

      # A SelectionMenu constructs a menu from a list of strings
      selection_menu_about = SelectionMenu([a_b, n, c_f])
      selection_menu_creators = SelectionMenu(["Andrii, andrii.holub82@gmail.com", "Natalia, sokilnatalka@gmail.com",
                                          "Oleksandr, a.chepkanich@gmail.com", "Tetiana, t_prischepa@ukr.net",
                                          "Yevhen, kossik89@gmail.com"])

      # A SubmenuItem lets you add a menu (the selection_menu above, for example)
      # as a submenu of another menu
      submenu_info = SubmenuItem(colored("Information", "yellow"), selection_menu_about, menu)
      submenu_creators = SubmenuItem(colored("Creators", "yellow"), selection_menu_creators, menu)

      # Once we're done creating them, we just add the items to the menu
      menu.append_item(address_book)
      menu.append_item(notes)
      menu.append_item(clean_folder)
      menu.append_item(submenu_info)
      menu.append_item(submenu_creators)

      # Finally, we call show to show the menu and allow the user to interact
      menu.show()

if __name__ == '__main__':
      main_menu()
