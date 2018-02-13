import sqlite3


class DataBaseIO():
    # this class should handle all of the sql work, and return only standard memory objects
    __db__ = None
    __cur__ = None

    def __init__(self, dbname):
        self.__db__ = sqlite3.connect(dbname)
        self.__cur__ = self.__db__.cursor()

    def _execute_sql_(self, sql=""):
        with self.__db__:
            statement = str(sql).replace(";", "")  # some effort to prevent hostile inputs
            self.__cur__.execute(statement)

    def spew_header(self, table_name):
        with self.__db__:
            cur = self.__cur__
            # https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
            column_names = [str(row[1]) for row in cur.execute("PRAGMA table_info({})".format(table_name)).fetchall()]
        return column_names

    def spew_tables(self):
        with self.__db__:
            # https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api
            tables = []
            tables_tup = self.__cur__.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            for each in tables_tup:
                tables.append(",".join(each))
        return tables

    def execute_query(self, table, select='*', parm='', regex=''):
        # returns data as a list, each row as a tuple
        if parm != '':
            results = self.__cur__.execute('select {} from {} where {} = {}'
                                           .format(select, table, parm, regex)).fetchall()
        else:
            results = self.__cur__.execute('select {} from {}'.format(select, table)).fetchall()
        return results

    def create_table(self, table_name, *args):
        with self.__db__:

            sql = """Create Table if not exists {} ({})""".format(table_name, "".join(args))
            self._execute_sql_(sql)

    def add_record(self, table_name, columns='', *args):
        """
        https://www.jetbrains.com/help/pycharm/creating-documentation-comments.html
        :param table_name: any single string
        :param columns: use '' for implicit entries
        :param args: all values to insert, i.e: "'1','foo'" or "'bar'"
        :return: void
        """
        if columns != '':
            sql = "insert into {} ({}) values ({})".format(table_name, "".join(columns), "".join(args))

        else:
            sql = "insert into {} values ({})".format(table_name, "".join(args))
        self._execute_sql_(sql)

    def update_record(self, table_name, column, unique_id="", new_value=""):
        """
        UPDATE table
        SET column_1 = new_value_1,
            column_2 = new_value_2
        WHERE
            search_condition
        """
        if unique_id != "":
            sql = "UPDATE {} SET {} = '{}' WHERE id = {}".format(table_name, column, new_value, unique_id)
            self._execute_sql_(sql)

    def delete_record(self, table_name, parm, regex=""):
        if regex != "":
            self._execute_sql_("delete from {} where {} = '{}'".format(table_name, parm, regex))
        else:
            print("Too broad of delete clause, aborting")

    def close(self):
        self.__db__ = None
