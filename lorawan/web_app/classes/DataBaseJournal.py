import sqlite3


class СlassDataBaseJournal():
    """
    Класс для работы с базой данных журнала событий
    """

    def __init__(self, path):
        self.path = path
        pass

    def open_database(self):
        # открыть БД
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        return connection, cursor

    def close_database(self, connection, cursor):
        # закрыть БД
        cursor.close()
        connection.close()

    def make_sign_journal(self, db_table, data):
        connection, cursor = self.open_database()
        cursor.execute(f"""
                            INSERT INTO {db_table} VALUES (?, ?, ?, ?, ?)
                            """, [data[0], data[1], data[2], data[3], data[4]])
        connection.commit()
        self.close_database(connection, cursor)
    
    def take_signs(self, db_table):
        try:
            connection, cursor = self.open_database()
            cursor.execute(f"""SELECT * FROM {db_table}""")
            sql_data = cursor.fetchall()
            self.close_database(connection, cursor)
            data = self.group_data_for_site(sql_data)
            return data
        except Exception as E:
            print(E)
            self.close_database(connection, cursor)
            return None
    
    def take_signs_by_condition(self, db_table, condition):
        try:
            connection, cursor = self.open_database()
            sqlstr = f"""SELECT * FROM {db_table} {condition}"""
            print(sqlstr)
            cursor.execute(sqlstr)
            sql_data = cursor.fetchall()
            self.close_database(connection, cursor)
            data = self.group_data_for_site(sql_data)
            return data
        except Exception as E:
            print(E)
            self.close_database(connection, cursor)
            return None


    def group_data_for_site(self, sql_data):
        data = []
        for i in sql_data:
            data.append(list(i))
        return data
    