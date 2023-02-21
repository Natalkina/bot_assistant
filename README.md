# PERSONAL ASSISTANT

## Installation

```
pip install personal-assistant-cli-bot
```


## General information 
To start work please enter the commmand in Terminal: pacb

Personal Assistant will help you to save you time in organisation of you work.

The main menu:
![Main menu](/docs/main_menu.jpg "Main menu")
To autocomplete the name of commands use Tab

### Addressbook
Module for working with your contacts, contain and work with information about contact:
"name", "phones", "birthday", "email", "address". 

#### Commands:
 * **'add'** For using please input user's name and phone to add the user
 * **'birthday'** For using please input user's name and birthday in format DD.MM.YYYY to add the birthday
 * **'days_to_birthday'** For using please input user's name, calculate the quantity of days till user's birthday
 * **'get_birthdays'** For using please input user's name, calculate number for searching users with birthdays in number days                         
 * **'change'** For using please input user's name and phone for changing the phone number
 * **'phone'**  For using please input user's name to phone
 * **'email'**  For using please input user's name and email to add the email
 * **'address'**  For using please input user's name and address to add the address
 * **'show_all'** Show some quantity of users on page. For using input how many pages you want to  see
 * **'delete'** For using please input user's name to delete the contact
 * **'save'** For saving the address book to 'address_book.csv' in current folder
 * **'get_book'** To get the address book from 'address_book.csv' in current folder
 * **'find'** For using please input some symbols to show data in the contacts with this symbols

#### Exit commands:
'goodbye', 'close', 'exit'
### Notebook
Module for working with notes, contain and work with information about notes:
"text", "tag", "id" - it is a creation time of note. 

#### Commands:

*  **'add'** - For using please input the note, which you want to add
*  **'edit'** - For using please input the ID, in which you want to edit note 
*  **'delete'** - For using please input the ID of note, which you want to delete 
*  **'showall'** - Show all notes
*  **'save'** - Save changes, which was done  during the session
*  **'sorted_date'** - Sorting by date from newer records and output
*  **'sorted_tag'** - Sorting tags alphabetically and output
#### Exit commands:
*  **'exit'** - exit the program.
### Clean Folder
Clean folder is the application which helps to sort folders.
To start please enter 3 for choosing the Clean Folder".
..
It sorts:
*	images ('JPEG', 'PNG', 'JPG', 'SVG', 'PSD' );
*	videos ('AVI', 'MP4', 'MOV', 'MKV');
*	documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'XLS');
*	music ('MP3', 'OGG', 'WAV', 'AMR');
*   books ('FB2', 'EPUB')
*   drawings ('DWG', 'DXF')
*   archives ('ZIP', 'GZTAR', 'TAR', 'BZTAR', 'XZTAR' );
*	apps('EXE', 'MSI')

Additional functions:
*   normalize cyrillic symbols to latin, other symbols to "_"
*   unpack all archives
*   delete empty folders

## Contacts
Our preferred channels of communication are all public, but if you’d like to speak to us in private first, contact us directly:
* "Andrii, andrii.holub82@gmail.com",
* "Natalia, sokilnatalka@gmail.com"
* "Oleksandr, a.chepkanich@gmail.com"
* "Tetiana, t_prischepa@ukr.net"
* "Yevhen, kossik89@gmail.com"
