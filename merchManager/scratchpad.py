from merchManager.DataBaseIO import DataBaseIO

dbio = DataBaseIO("test.db")
dbio.create_table("test_list", "id INTEGER PRIMARY KEY, entry TEXT")
dbio.add_record("test_list", 1, ",test")
list = dbio.execute_query("test_list")
