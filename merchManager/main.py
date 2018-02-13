from merchManager.DataBaseIO import DataBaseIO
from datetime import date

# connect and make connection available to program
database = DataBaseIO('sales.db')
inventory = "inventory"
sales = "sales"
venues = "venues"


def wip():
    # small method to toss into unfinished functions
    print("This method is currently still a work in progress\n"
          "Bug the Author to get this finished\n")


def initialize():

    # add inventory storage (if the persistant database doesn't already have a table)

    database.create_table(inventory,
                          "id INTEGER PRIMARY KEY, "
                          "name TEXT NOT NULL, "
                          "description TEXT,"
                          "price NUMERIC,"
                          "quantity INTEGER")  # inventory

    # add venue storage
    database.create_table(venues,
                          "id INTEGER PRIMARY KEY, "
                          "name TEXT,"
                          "contact TEXT,"
                          "street TEXT,"
                          "city TEXT,"
                          "state TEXT,"
                          "zip TEXT,"
                          "phone TEXT")  # venues

    # add sales data storage
    database.create_table(sales,
                          "id INTEGER PRIMARY KEY, "
                          "venue_id INTEGER, "
                          "date TEXT, "
                          "product_id INTEGER,"
                          "product_qty INTEGER,"
                          "FOREIGN KEY(venue_id) REFERENCES venues(id),"
                          "FOREIGN KEY(product_id) REFERENCES inventory(id)")  # sales


def query_venue():
    print("Search by which parameter?\n(hit enter for all venues)")
    parm = ""
    data = []
    # sanitize inputs via code, not the greatest as this should be done in the class instead
    field = str(input(", ".join(database.spew_header(venues)[1:]) + "\n")).strip("'").strip(";")
    if field.strip() != "":
        parm = input("value to find for " + field + "? ")
    # lookup venue details
    if parm == "":
        data = [str(each) for each in database.execute_query(venues)]
    else:
        if field in database.spew_header(venues):
            data = [str(each) for each in database.execute_query(venues, '*', field, "'{}'".format(parm))]
        else:
            print(database.spew_header(venues))
    return data


def get_sales():
    print("Search by which parameter?\n(hit enter for all venues)")
    parm = ""
    data = []
    field = str(input(", ".join(database.spew_header(sales)[1:]) + "\n"))
    if field.strip() != "":
        parm = input("value to find for " + field + "? ")
    # lookup venue details
    if parm == "":
        data = database.execute_query(sales)
    else:
        if field in database.spew_header(sales):
            data = database.execute_query(sales, '*', field, "'{}'".format(parm))
        else:
            print(database.spew_header(sales))
    return data


def report_sales():
    data_list = []
    for each in database.spew_header(sales)[1:]:
        if each == "date":
            value = input("please enter a value for: {}\n"
                          "leave blank to insert {}".format(each, date.today()))
            if value.strip() != "":
                data_list.append("'{}'".format(value))
            else:
                data_list.append("'{}'".format(date.today()))
        else:  # hold user in loop to not insert null value
            value = ""
            while value == "":
                value = input("please enter a value for: {}\n".format(each))
            data_list.append("'{}'".format(value))
    data = ", ".join(data_list)
    database.add_record(sales, database.spew_header(sales)[1:], data)


def add_inventory():
    data_list = []
    for each in database.spew_header(inventory)[1:]:
        value = ""
        while value == "":
            value = input("please enter a value for: {}\n".format(each))
        data_list.append("'{}'".format(value))
    data = ", ".join(data_list)
    database.add_record(inventory, ",".join(database.spew_header(inventory)[1:]), data)


def get_inventory():
    print("Search by which parameter?\n(hit enter for all inventory)")
    parm = ""
    data = [",".join(database.spew_header(inventory))]
    # sanitize inputs via code, not the greatest as this should be done in the class instead
    field = str(input(", ".join(database.spew_header(inventory)[1:]) + "\n")).strip("'").strip(";")
    if field.strip() != "":
        parm = input("value to find for " + field + "? ")
    # lookup venue details
    if parm == "":
        for each in database.execute_query(inventory):
            data.append(str(each))
    else:
        if field in database.spew_header(inventory):
            for each in database.execute_query(inventory, '*', field, "'{}'".format(parm)):
                data = str(each)
        else:
            print(database.spew_header(inventory))
    return data


def add_venue():
    data_list = []
    for each in database.spew_header(venues)[1:]:
        value = ""
        while value == "":
            value = input("please enter a value for: {}\n".format(each))
        data_list.append("'{}'".format(value))
    data = ", ".join(data_list)
    database.add_record(venues, ",".join(database.spew_header(venues)[1:]), data)


def menu(choices):
    # https://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops
    # small function to parse a comma delimited string into a list of menu options, always puts the exit
    # option as the final choice, equal to the size of the original argument split into a list
    # ie "" would have exit as option 1 (there's probably an even better way to do procedural menus)
    choices += ",Exit"

    for index, item in enumerate(choices.split(',')):
        print("{}: {}".format(str(index + 1), item))
    try:
        selection = int(input("Please select an option"))
        print(selection)
        if 0 < selection-1 < len(choices.split(',')):
            return selection
        else:
            return -1
    except ValueError:
        return -1


def main():
    # functions should return data here, main should handle the final display logic
    initialize()
    choices = \
        "Show sales by date(s)," \
        "Show venue(s)," \
        "Show products," \
        "Add product," \
        "Add venue," \
        "Add sales data"
    option = 0
    while option <= len(choices.split(',')):
        option = menu(choices)
        if option <= 0:
            print("Invalid selection\n")
            main()

        else:
            if option == 1:
                get_sales()

            elif option == 2:
                print("\n".join(query_venue()))

            elif option == 3:
                print("\n".join(get_inventory()))

            elif option == 4:
                add_inventory()

            elif option == 5:
                add_venue()

            elif option == 6:
                report_sales()


if __name__ == '__main__':
    main()
