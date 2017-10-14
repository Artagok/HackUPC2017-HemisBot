# -*- coding: utf-8 -*-

import sqlite3

class DBHelper:

    # connect to the db:
    def __init__(self, dbname = "pollution.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # create the table and indexes. Info stored for item: description + author
    def setup(self):
        table1 = "CREATE TABLE IF NOT EXISTS items (description text, author text)"
        indexItem = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        indexAuthor = "CREATE INDEX IF NOT EXISTS authorIndex ON items (author ASC)"
        self.conn.execute(table1)
        self.conn.execute(indexItem)
        self.conn.execute(indexAuthor)
        self.conn.commit()

    # obtain values and process them
    def get_items(self, author):
        stmt = "SELECT description FROM items WHERE author = (?)"
        args = (author, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    # add items into db to be stores
    def add_item(self, item_text, author):
        stmt = "INSERT INTO items (description, author) VALUES (?, ?)"
        args = (item_text, author)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # deltes an item from the db
    def delete_item(self, item_text, author):
        stmt = "DELETE FROM items WHERE description = (?) AND author = (?)"
        args = (item_text, author )
        self.conn.execute(stmt, args)
        self.conn.commit()
