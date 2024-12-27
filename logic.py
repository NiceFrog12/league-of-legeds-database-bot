import sqlite3
from config import DATABASE

class DBManager():
    def __init__(self, database):
        self.database = database


    def get_champion_stats(self, champion_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM table1 WHERE Name = ?", (champion_name,)) #values: Champname, Class, Role, Tier (F-S/God), Score, Trend, WR%, Role%, Pickrate, Banrate, average KDA
            return cur.fetchall()
    def get_misc_stats(self, champion_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM table0 WHERE Name = ?", (champion_name,)) #values: ID, Champname, Class, Style, Difficulty, DamageType, Damage, Sturdiness, Crowd_control, Mobility, Functionality
            return cur.fetchall()
    def get_champion_off_stat(self, misc_stat, stat_value):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f"SELECT Name FROM table0 WHERE {misc_stat} = ?", (stat_value,))
            return cur.fetchall()
    def get_champion_off_role(self, rolename):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT Name FROM table1 WHERE Role = ?", (rolename,))
            return cur.fetchall()

if __name__ == '__main__':
    manager = DBManager(DATABASE)