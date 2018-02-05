import sqlite3


class DataBaseIO():
    __db__ = None
    __cur__ = None
    WIP = "This feature is not yet implemented"

    def __init__(self, dbname):
        self.__db__ = sqlite3.connect(dbname)
        self.__cur__ = self.__db__.cursor()

    def _execute_sql_(self, sql=""):
        with self.__db__:
            statement = str(sql)
            self.__cur__.execute(statement)

    def spew_header(self, table_name):
        with self.__db__:
            cur = self.__cur__
            # https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
            column_names = [str(row[1]) for row in cur.execute("PRAGMA table_info(?)", table_name).fetchall()]
        return column_names

    def spew_tables(self):
        with self.__db__:
            # https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api
            tables = [self.__cur__.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        return tables

    def execute_query(self, table, select='*', parm='', regex=''):

        if parm != '':
            results = [self.__cur__.execute('select ? from ? where ? = ?',(select, table, parm, regex))]
        else:
            results = [self.__cur__.execute('select ? from ?',(select,table))]
        return results

    def create_table(self, table_name, *args):
        """
        CREATE TABLE contacts (
        contact_id integer PRIMARY KEY,
        first_name text NOT NULL,
        last_name text NOT NULL,
        email text NOT NULL UNIQUE,
        phone text NOT NULL UNIQUE
        );
        """
        self.__cur__.execute('Create Table ? ( ? )', (table_name, args))

    def add_record(self, table_name, *args):
        self.__cur__.execute('insert into ' + table_name + ' Values ' + str(*args))
        print(self.WIP)

    def update_record(self):
        print(self.WIP)

    def delete_record(self, table_name, parm, regex):
        self.__cur__.execute("delete from ? where ? = ?", (table_name, parm, regex))

    def close(self):
        self.__db__ = None
