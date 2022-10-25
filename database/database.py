import sqlite3


class SqliteDB:

    def __init__(self):

        pass

        # this runs at first time of the db creation
        # self.firsttimerun()


    def firsttimerun(self):
        # Database connection
        con = self.createDatabaseConnection()
        cur = con.cursor()

        try:

            cur.execute('''CREATE TABLE users (
               USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               NAME text,
               INSTA_ID text
           )''')
            print("Users Table Created")
            cur.execute('''CREATE TABLE following (
                       PERSON_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       NAME text,
                       INSTA_ID text,
                       USER_ID INTEGER,
                       CONSTRAINT fk_users
                           FOREIGN KEY (USER_ID)
                           REFERENCES users(USER_ID)

                   )''')
            print("follwing persons table Created")

        except Exception as e:
            print(f"Error in table creation:={e}")
            cur.close()
            con.close()
        finally:
            con.commit()
            cur.close()
            con.close()

    # add user into user table,we list the followers from this user
    def adduser(self, instaperson):

        con = self.createDatabaseConnection()
        cur = con.cursor()
        try:

            sql = '''INSERT INTO users (NAME,INSTA_ID) VALUES(?,?)'''
            cur.execute(sql, [instaperson.NAME,instaperson.INSTA_ID])
            print(f"Successfully added user:{instaperson.tostring()}")
        except Exception as e:
            print(f"Coudnt insert user into db:={e}")
            cur.close()
            con.close()
        finally:
            con.commit()
            con.close()

    def createDatabaseConnection(self):
        db_file = r'database/instagram.db'
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Exception as e:
            print(f"Databse connection failed:={e}")

        return conn


if __name__ == "__main__":
    ##database instance creation
    db = SqliteDB()
