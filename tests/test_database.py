from unittest import TestCase, main
from merchManager.DataBaseIO import DataBaseIO
from os import remove, listdir


class TestMain(TestCase):
    database = None
    cursor = None

    def setUp(self):
        print('setup_test')
        # setup the database, connection, and cursor,
        # if this fails verify class init method working properly and
        # all arguments passed to init correctly

        self.database = DataBaseIO('test.db')
        self.cursor = self.database.__cur__

    def tearDown(self):
        print('teardown_test')
        pass

    @classmethod
    def setUpClass(cls):
        # remove old test data each time so we start fresh.
        # doesn't work to remove at teardown class as db is
        # apparently still in use during runtime?
        print('setup_class\n')
        database_name = "test.db"
        if str(listdir(".")).find(database_name) >= 0:
            remove(database_name)
        pass

    @classmethod
    def tearDownClass(cls):
        print('teardown_class')

    def test_null(self):
        print("test_null")
        # basic reminder notes on unit test, literally a test test.
        # in all reality, this test should never fail.
        # if this test fails, then reality might be broken.
        val1 = None
        val2 = None
        self.assertEqual(val1, val2)

    def test_crud(self):
        # full crud test w/ a table
        # check that we can add a table w/ some data
        print("self.test_spew()")
        table_name = "test_table"

        # CREATE
        self.database.create_table(table_name, "id INTEGER PRIMARY KEY AUTOINCREMENT, some_text TEXT")
        self.assertIn("test_table", str(self.database.spew_tables()))
        # check that added table has columns
        self.assertIn("id", self.database.spew_header(table_name))
        # self.database.spew_header(table_name)
        # add explicit data
        self.database.add_record(table_name, '', "'1','foo'")
        # add implicit data
        self.database.add_record(table_name, "some_text", "'bar'")
        # add more explicit data
        self.database.add_record(table_name, '', "'3','foobar'")
        # READ
        results = list(self.database.execute_query(table_name))
        # print(results)
        # check if record present
        self.assertIn("foo", str(results))

        # UPDATE try testing a change to a record
        self.database.update_record(table_name, "some_text", "1", "fu")
        results = list(self.database.execute_query(table_name))
        # print(results)
        self.assertIn("fu", str(results))

        # DELETE deleting test
        self.database.delete_record(table_name, 'some_text', 'fu')
        results = list(self.database.execute_query(table_name))
        # print(results)
        self.assertNotIn("fu", str(results))


if __name__ == '__main__':
    main()
