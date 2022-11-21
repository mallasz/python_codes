import mysql.connector as database
import traceback


class DB:
    """
    Database access class. This uses MariaDB or MySQL.
    """

    default_connection_parameters = {'user': 'eduard',
                                     'password': 'eduard12',
                                     'host': 'localhost',
                                     'database': 'eduard'}
    """
    These are the default connection parameters. Everything can be modified in the constructor.
    """

    def __init__(self, **kwargs):
        """
        Constructor, handles connection parameters and connects to the DB.
        :param kwargs: Parameters to override, e.g. user="root" instead of "eduard"
        """
        self.connection_parameters = self.default_connection_parameters | kwargs  # dict "union"/override
        self.connection = database.connect(**self.connection_parameters)  # connects to DB
        # since parameters are in a dict, ** needed.

    def reconnect(self):
        """
        Disconnects and reconnects to the database.
        :return: None
        """
        if self.connection:
            self.connection.disconnect()
        self.connection = database.connect(**self.connection_parameters)

    def get_data(self, sql_text, params=()):
        """
        Executes a DB query
        :param sql_text: SQL statement with %s placeholders
        :param params: optional tuple to be put into the statement
        :return: list of lists with the query results
        (outer list holds the rows, and the rows are also lists themselves)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_text, params)
            return cursor.fetchall()
        except database.Error as e:
            print(f"Error retrieving entry from database: {e}")
            print(str(traceback.format_exc()))
            return None

    def do_command(self, sql_text, params=()):
        """
        Executes a DB command (e.g. insert)
        :param sql_text: SQL statement with %s placeholders
        :param params: optional tuple to be put into the statement
        :return: bool, True on success
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(sql_text, params)
                self.commit()
                return True
        except database.Error as e:
            print(f"Error retrieving entry from database: {e}")
            print(str(traceback.format_exc()))
            self.rollback()
            return False

    def commit(self):
        """Commit previous operations"""
        self.connection.commit()
        return True

    def rollback(self):
        """Rollback previous operations"""
        self.connection.rollback()
        return True

    def load_file(self, file_name):
        """
        Reads an SQL file line by line, and sends it command by command to the database.
        :param file_name: the name of the SQL file
        :return: None
        """
        with open(file_name, 'r', encoding='utf-8') as f:
            command = ''
            while line := f.readline():
                command += line
                if command.endswith(';\n'):
                    # Sample SQL file had ';' characters inside the insert statements.
                    # this one works in that case as well
                    self.do_command(command)
                    command = ''

    def reset_database(self):
        """
        A simple way to load original database.
        This prevents from identical student names, usernames, empty datasets after too many deletes, etc.
        Test cases can be independent this way.
        :return:
        """
        self.load_file('../test_config/eduard.sql')
