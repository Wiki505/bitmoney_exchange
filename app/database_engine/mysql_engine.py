from mysql.connector import connect

class bitmoney_exchange():
    """ This class define the MySQL process for all engine """
    def __init__(self, database_name):
        self.mysql_connector = connect(user='root', host='192.168.64.2', password='compass', database='bitmoney_exchange')
        self.cursor = self.mysql_connector.cursor()

    def read(self, mysql_query):
            self.cursor.execute('''%s''' % mysql_query)
            data = self.cursor.fetchall()
            self.cursor.close()
            return data

    def write(self, mysql_query):
        self.cursor.execute('''%s''' % mysql_query)
        self.mysql_connector.commit()
        self.cursor.close()
        return True

class bitmoney_network():
    """ This class define the MySQL process for all engine """
    def __init__(self, database_name):
        self.mysql_connector = connect(user='root', host='192.168.64.2', password='compass', database='bitmoney_network')
        self.cursor = self.mysql_connector.cursor()

    def read(self, mysql_query):
            self.cursor.execute('''%s''' % mysql_query)
            data = self.cursor.fetchall()
            self.cursor.close()
            return data

    def write(self, mysql_query):
        self.cursor.execute('''%s''' % mysql_query)
        self.mysql_connector.commit()
        self.cursor.close()
        return True