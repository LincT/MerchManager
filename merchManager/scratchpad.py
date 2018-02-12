from merchManager.DataBaseIO import DataBaseIO
from os import remove, listdir

database_name = "test.db"
if str(listdir(".")).find(database_name) >= 0:
    remove(database_name)
dbio = DataBaseIO("test.db")
dbio.create_table("test_list", "id INTEGER PRIMARY KEY, entry TEXT")
dbio.add_record("test_list", "'1', 'test'")
list = dbio.execute_query("test_list")
print(dbio.spew_tables())
print(list)
