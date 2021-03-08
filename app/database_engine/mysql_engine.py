from mysql.connector import connect

class run_database():
    """ This class define the MySQL process for all engine """
    def __init__(self):
        self.mysql_connector = connect(user='root', host='127.0.0.1', password='compass', database='bitmoney_network')
        self.cursor = self.mysql_connector.cursor()

    def read(self, mysql_query):
            self.cursor.execute(mysql_query)
            data = self.cursor.fetchall()
            self.cursor.close()
            return data

    def write(self, mysql_query):
        self.cursor.execute(mysql_query)
        self.mysql_connector.commit()
        self.cursor.close()
        return True
