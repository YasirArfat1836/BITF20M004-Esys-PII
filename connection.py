import pymysql


class Connection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def MakeConnection(self):
        return pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
