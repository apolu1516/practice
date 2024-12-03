# [import p01_1da_sales and use alias sd]

import csv
# [import class Decimal and constant ROUND_HALF_UP from decimal library]
from decimal import Decimal, ROUND_HALF_UP
import p01beg_1da_sales as sd 
import locale as lc

lc.setlocale(lc.LC_ALL, "en_US")


# [Add code to handle exception FileNotFoundError by displaying "Sales file not found"]
def import_all_sales() -> list:
    try:
        with (open(sd.FILEPATH / sd.ALL_SALES, newline='') as csvfile):
            reader = csv.reader(csvfile)
            sales_list = []
            for line in reader:
                if len(line) > 0:
                    *amount_sales_date, region_code = line
                    sd.correct_data_types(amount_sales_date)
                    amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                    data = {"amount": amount,
                            "sales_date": sales_date,
                            "region": region_code,
                            }
                    sales_list.append(data)
            return sales_list  # within with statement
    except FileNotFoundError:
        print("Sales file not found.")
        return []


# [Modify the code to use Decimal of decimal library and currency function of the locale library ]
def view_sales(sales_list: list) -> bool:
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.\n")
    else:  # not empty
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15
        total_w = col1_w + col2_w + col3_w + col4_w + col5_w
        print(f"{' ':{col1_w}}"
              f"{'Date':{col2_w}}"
              f"{'Quarter':{col3_w}}"
              f"{'Region':{col4_w}}"
              f"{'Amount':>{col5_w}}")
        print(horizontal_line := f"{'-' * total_w}")

        # Initialize total as a Decimal
        total = Decimal("0")

        for idx, sales in enumerate(sales_list, start=1):
            if sd.has_bad_data(sales):
                bad_data_flag = True
                num = f"{idx}.*"   # add period and asterisk
            else:
                num = f"{idx}."   # add period only

            #amount = Decimal(sales["amount"]).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
            try:
                amount = Decimal(sales["amount"]).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
            except Exception as e:
                print(f"Error processing amount: {e}")
                continue  # Skip this record if there's an error

            if not sd.has_bad_amount(sales):
                total += amount

            sales_date = sales["sales_date"]
            if sd.has_bad_date(sales):
                bad_data_flag = True
                month = 0
            else:
                print(sales_date)
                month = sales_date.month
            # Get region name and quarter
            region = sd.get_region_name(sales["region"])
            quarter = f"{sd.cal_quarter(month)}"

            # Format amount as currency
            formatted_amount = lc.currency(amount, grouping=True)

            # Print sales data
            print(f"{num:<{col1_w}}"
                  f"{sales_date:{col2_w}}"
                  f"{quarter:<{col3_w}}"
                  f"{region:{col4_w}}"
                  f"{formatted_amount:>{col5_w}}")

        # Print total
        formatted_total = lc.currency(total, grouping=True)
        print(horizontal_line)
        print(f"{'TOTAL':{col1_w}}"
              f"{' ':{col2_w + col3_w + col4_w}}"
              f"{formatted_total:>{col5_w}}\n")
    return bad_data_flag


def add_sales1(sales_list) -> None:
    sales_list.append(data := sd.from_input1())
    print(f"Sales for {data["sales_date"]} is added.\n")


def add_sales2(sales_list) -> None:
    sales_list.append(data := sd.from_input2())
    print(f"Sales for {data["sales_date"]} is added.\n")


# [Modify the code accordingly to use objects from other module]

# [Modify the code accordingly to use objects from other module]
def import_sales(sales_list) -> None:
    # get filename from user
    filename = input("Enter name of file to import: ")
    filepath_name = sd.FILEPATH / filename
    # check if filename is valid
    if not sd.is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of '{sd.NAMING_CONVENTION}'.")
    # check if region code (the 5th character from end) is valid.
    elif not sd.is_valid_region(sd.get_region_code(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(sd.VALID_REGIONS.keys())}.")
    # check if file has already been imported
    elif sd.already_imported(filepath_name):
        filename = filename.replace("\n", "")  # remove new line character
        print(f"File '{filename}' has already been imported.")
    else:
        # import sales data from file
        try:
            imported_sales_list = sd.import_sales(filepath_name)# function in the imported module
            if imported_sales_list is None:
                print(f"Failed to import sales from '{filename}'. The import returned None.")
                return
        except Exception as e:  
            print(f"{type(e)}. Fail to import sales from '{filename}'.")
        else:
            # display imported sales
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                     "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:  
                sales_list.extend(imported_sales_list)    
                print("Imported sales added to list.")
                sd.add_imported_file(filepath_name)



# [Modify the code to raise and handle exception(s)]
def save_all_sales(sales_list: list, delimiter: str = ',') -> None:
    # convert the list of Sales to a list of lists of sales data (amount, sales_date, region.code), using comprehension
    sales_records = [[sales["amount"], f"{sales["sales_date"]:{sd.DATE_FORMAT}}", sales["region"]]
                     for sales in sales_list]
    try:
        with open(sd.FILEPATH / sd.ALL_SALES, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)

            ''' The following additional code is only for practicing raising 
            exception for testing purpose, and will be commented out for 
            testing whether the function can save data successfully.
            You will write code to do the following:
            - Write a try clause in which raise an OSError.
            - Reraise the OSError in the except clause that handles the OSError exception.
            - Write code to make sure the csvfile is closed no matter an exception occurs or not.
            - Optionally, you may also add code to roll back the change to the imported_files]
            '''
            ...

            writer.writerows(sales_records)
            print("Saved sales records.")
    except OSError as e:
        print(f"OSError: {e}. Sales data could not be saved.")
    except Exception as e:
        print(f"Error: {type(e)}. Sales data could not be saved.")

def main():
  '''
  Write code to test the functions in this module
  '''
  # Test importing sales data
  print("Importing sales data...")
  sales_list = import_all_sales()  # Assuming this function is correctly implemented and returns a list of sales

  # Test adding sales data
  print("Adding sales data...")
  add_sales1(sales_list)  # Or you could use add_sales2 depending on the input method

  # Test viewing the sales data
  print("Viewing sales data...")
  bad_data_flag = view_sales(sales_list)  # Returns True if bad data is found
  if bad_data_flag:
      print("There was an issue with some of the sales data.")
  else:
      print("Sales data displayed successfully.")

  # Test saving the sales data
  print("Saving sales data...")
  save_all_sales(sales_list)  # Assuming this function handles saving to a file


if __name__ == "_main_":
    main()
