
import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, name):
        self.name = (name, )
        self.con = self.sql_connection()

    def sql_connection(self):
        try:
            con = sqlite3.connect(self.name[0])
            return con

        except Error:
            print(Error)

    def sql_table(self):
        cursorObj = self.con.cursor()

        cursorObj.execute(
            'create table if not exists board(id integer PRIMARY KEY, piece0 text, piece1 text,'
            ' piece2 text,piece3 text,piece4 text,piece5 text,'
            'piece6 text,piece7 text)'
        )

        self.con.commit()

    def sql_insert(self, entity):
        cursorObj = self.con.cursor()

        cursorObj.execute(
            'INSERT INTO board(id, piece0, piece1, piece2, piece3, piece4, piece5, piece6, piece7)'
            ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', entity)

        self.con.commit()

    def sql_drop(self):
        cursorObj = self.con.cursor()

        cursorObj.execute('drop table if exists board')

        self.con.commit()

    def sql_delete(self):
        cursorObj = self.con.cursor()

        cursorObj.execute('Delete from board')

        self.con.commit()

    def sql_fetch(self):
        cursorObj = self.con.cursor()
        cursorObj.execute('SELECT * FROM board')

        rows = cursorObj.fetchall()

        return rows

    def doesDataExist(self):
        cursorObj = self.con.cursor()

        cursorObj.execute('SELECT * FROM board' )
        if(cursorObj.fetchall() ==[(0, 'br', 'bk', 'bb', 'bq', 'bking', 'bb', 'bk', 'br'),
                                      (1, 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'),
                                      (2, '', '', '', '', '', '', '', ''),
                                      (3, '', '', '', '', '', '', '', ''),
                                      (4, '', '', '', '', '', '', '', ''),
                                      (5, '', '', '', '', '', '', '', ''), (6, 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'), (7, 'wr', 'wk', 'wb', 'wq', 'wking', 'wb', 'wk', 'wr')]


        ):

            print("SS")
            return False

        else:
            return True


class DatabaseTurn:
    def __init__(self):
        self.con = self.sql_connection()

    def sql_connection(self):
        try:
            con = sqlite3.connect("countsave.db")
            return con

        except Error:
            print(Error)

    def sql_table(self):
        cursorObj = self.con.cursor()

        cursorObj.execute(
            'create table if not exists count(id integer PRIMARY KEY, turn integer)'
        )

        self.con.commit()

    def sql_insert(self, entity):
        cursorObj = self.con.cursor()

        cursorObj.execute(
            'INSERT INTO count(id, turn)'
            ' VALUES(?, ?)', entity)

        self.con.commit()

    def sql_drop(self):
        cursorObj = self.con.cursor()

        cursorObj.execute('drop table if exists count')

        self.con.commit()

    def sql_delete(self):
        cursorObj = self.con.cursor()

        cursorObj.execute('Delete from count')

        self.con.commit()

    def sql_fetch_count(self):
        cursorObj = self.con.cursor()
        cursorObj.execute('SELECT * FROM count')
        rows = cursorObj.fetchall()
        return rows[0][1]