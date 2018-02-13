from merchManager.DataBaseIO import DataBaseIO
from os import remove, listdir
from datetime import date

database_name = "test.db"
# comment the next two lines out to see the database keep acumulating new entries
if str(listdir(".")).find(database_name) >= 0:
    remove(database_name)
dbio = DataBaseIO("test.db")
dbio.create_table("test_list", "id INTEGER PRIMARY KEY, entry TEXT, float NUMERIC")
dbio.add_record("test_list", 'entry,float', "'test', 1.5")
my_list = dbio.execute_query("test_list")
value = dbio.execute_query("test_list", 'float', 'id', '1')[0][0]

choices = \
    "Show sales by date(s)," \
    "Show venue(s)," \
    "Add product," \
    "Add venue," \
    "Add sales data," \
    "Exit"

# https://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops

choice_list = [item for item in choices.split(',')]
for index, item in enumerate(choices.split(',')):
    print("{}: {}".format(str(index + 1), item))
print("math test: "+str(value*2))
print("\n".join(dbio.spew_tables()))
print(", ".join(dbio.spew_header("test_list")))
print(date.today())
for each in my_list:
    print(", ".join([str(item) for item in each]))
