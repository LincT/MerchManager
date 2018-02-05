from unittest import TestCase, main
from merchManager.DataBaseIO import DataBaseIO
from os import remove


class TestMain(TestCase):
    db = None
    cur = None

    def setUp(self):
        print('setup_test')
        self.db = DataBaseIO('test.db')
        self.cur = self.db.__cur__

    def tearDown(self):
        print('teardown_test')
        pass

    @classmethod
    def setUpClass(cls):
        print('setup_class\n')
        remove("test.db")
        pass

    @classmethod
    def tearDownClass(cls):
        print('teardown_class')


    def test_null(self):  # basic reminder notes on unit test, literally a test test
        print("self.test_null()")
        self.assertEqual(None, None)

    def test_spew(self):
        print("self.test_spew()")
        self.db.create_table("test_table", "id INTEGER, name TEXT")
        print(str(self.db.spew_tables()))
        pass


if __name__ == '__main__':
    main
