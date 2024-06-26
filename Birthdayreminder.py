import csv
from datetime import datetime, timedelta
import pywhatkit as kit
import pyautogui
import time
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = r'C:\Users\home\Desktop\Web Scraping\birthdays.csv'

def read_birthdays(file_path):
    birthdays = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            name, date_str = row
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            birthdays.append((name, date))
    return birthdays

def write_birthdays(file_path, birthdays):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Date'])
        for name, date in birthdays:
            writer.writerow([name, date.strftime('%Y-%m-%d')])

def add_birthday(file_path, name, date_str):
    birthdays = read_birthdays(file_path)
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    birthdays.append((name, date))
    write_birthdays(file_path, birthdays)
    print(f"Added birthday for {name} on {date_str}")

def remove_birthday(file_path, name):
    birthdays = read_birthdays(file_path)
    birthdays = [entry for entry in birthdays if entry[0] != name]
    write_birthdays(file_path, birthdays)
    print(f"Removed birthday for {name}")

def edit_birthday(file_path, name, new_date_str):
    birthdays = read_birthdays(file_path)
    new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
    for i, (entry_name, entry_date) in enumerate(birthdays):
        if entry_name == name:
            birthdays[i] = (name, new_date)
            write_birthdays(file_path, birthdays)
            print(f"Edited birthday for {name} to {new_date_str}")
            return
    print(f"Birthday for {name} not found")

def check_upcoming_birthdays(birthdays, days=7):
    upcoming = []
    today = datetime.now().date()
    for name, date in birthdays:
        birthday_this_year = date.replace(year=today.year)
        if 0 <= (birthday_this_year - today).days <= days:
            upcoming.append((name, birthday_this_year))
    return upcoming

def send_whatsapp_message(message, to_whatsapp_number):
    now = datetime.now()
    hour = now.hour
    minute = (now.minute + 2) % 60
    if now.minute + 2 >= 60:
        hour = (hour + 1) % 24

    
    kit.sendwhatmsg(to_whatsapp_number, message, hour, minute)

    
    time.sleep(20)  

 
    pyautogui.press('enter')

def main():
    birthdays = read_birthdays(file_path)
    upcoming_birthdays = check_upcoming_birthdays(birthdays)

     
    my_whatsapp_number = '+1234567890'  # Your WhatsApp number including the country code.

    for name, date in upcoming_birthdays:
        message = f"Reminder: {name}'s birthday is on {date.strftime('%Y-%m-%d')}."
        send_whatsapp_message(message, my_whatsapp_number)
        print(f"Sent reminder for {name}'s birthday on {date}")

    while True:
        print("\nBirthday Reminder Menu:")
        print("1. Add Birthday")
        print("2. Remove Birthday")
        print("3. Edit Birthday")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            date_str = input("Enter date (YYYY-MM-DD): ")
            add_birthday(file_path, name, date_str)
        elif choice == '2':
            name = input("Enter name to remove: ")
            remove_birthday(file_path, name)
        elif choice == '3':
            name = input("Enter name to edit: ")
            new_date_str = input("Enter new date (YYYY-MM-DD): ")
            edit_birthday(file_path, name, new_date_str)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
