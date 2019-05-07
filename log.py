"""
Programmer: JR Padfield
Description: Handles logging of the information from the obd2 to a database
Version: 1
Date: 05/07/2019
"""

import sqlite3 as db
import os


class ObdLogging:

    def __init__(self):
        self.conn = None

    def connect(self):
        """ Creates a connection to the sqlite database. """
        self.conn = db.connect('obdii.db')

    def disconnect(self):
        """ Closes the connection. """
        self.conn.close()

    def insert(self):
        """ Inserts data into the database. """
        pass

    def update(self):
        """ Updates the data in the database. """
        pass

    def delete(self):
        """ Deletes objects from the database."""
        pass

    def check_for_db(self):
        """ Checks to see if the database is created. If not it will create the database and tables for us. """
        exists = os.path.isfile('obdii.db')

        if not exists:
            # connect to the database so the obdii.db file is created.
            self.connect()
            # create tables in the database file.
            self.create_tables()
            # disconnect from the connection as we dont need it anymore.
            self.disconnect()

    def create_tables(self):
        """ Creates the database tables for us. """
        # create the cursor to execute the creation of the tables.
        cur = self.conn.cursor()

        # have the cursor execute the commands
        cur.execute('''CREATE TABLE Speed (uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, speed REAL, date NUMERIC)''')

        cur.execute('''CREATE TABLE RPM (uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, RPM REAL, date NUMERIC)''')

        cur.execute('''CREATE TABLE OilTemp (uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, temp REAL, date NUMERIC)''')

        cur.execute('''CREATE TABLE CoolantTemp (uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, temp REAL, date NUMERIC)''')

        cur.execute('''CREATE TABLE IntakeTemp (uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, temp REAL, date NUMERIC)''')

        cur.execute('''CREATE TABLE EngineLoad (uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, load REAL, date NUMERIC)''')


