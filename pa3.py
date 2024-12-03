# [Import all objects from the p01_2bl_salesmanager module]
import p01beg_2bl_salesmanager as sm # type: ignore
import p01beg_1da_sales as sd # type: ignore
from datetime import date, datetime

def display_title():
    print("SALES DATA IMPORTER\n")


def display_menu():
    cmd_format = "6"  # ^ center, < is the default for str.
    print("COMMAND MENU",
          f"{'view':{cmd_format}} - View all sales",
          f"{'add1':{cmd_format}} - Add sales by typing sales, year, month, day, and region",
          f"{'add2':{cmd_format}} - Add sales by typing sales, date (YYYY-MM-DD), and region",
          f"{'import':{cmd_format}} - Import sales from file",
          f"{'menu':{cmd_format}} - Show menu",
          f"{'exit':{cmd_format}} - Exit program", sep='\n')


# [Write code to ask user to enter a command and call corresponding functions[ 


def execute_command(sales_list) -> None:
    while True:
        command = input("Please enter a command: ").strip().lower()
        if command == "view":
            sm.view_sales(sales_list)
        elif command == "add1":
            sm.add_sales1(sales_list)
        elif command == "add2":
            sm.add_sales2(sales_list)
        elif command == "import":
            sm.import_sales(sales_list)
        elif command == "menu":
            display_menu()
        elif command == "exit":
            print("Exiting program.")
            break
        else:
            print("Invalid command. Please try again.")

def main():
    display_title()
    display_menu()

    # get all original sales data from a csv file
    sales_list = sm.import_all_sales()

    execute_command(sales_list)

    print("Bye!")


# if started as the main module, call the main function
if __name__ == "_main_":
    main()