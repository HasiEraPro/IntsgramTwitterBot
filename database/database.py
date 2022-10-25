import sqlite3


class SqliteDB:

    def __init__(self):
        # Database
        con = sqlite3.connect('instagram.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE users (
            USER_ID INTEGER PRIMARY KEY INCREMENT,
            NAME text,
            INSTA_ID text, 
        )''')

        cur.execute('''CREATE TABLE following (
                    PERSON_ID INTEGER PRIMARY KEY INCREMENT,
                    NAME text,
                    INSTA_ID text,
                    CONSTRAINT fk_departments
                        FOREIGN KEY (USER_id)
                        REFERENCES users(USER_ID)
                     
                )''')

        con.commit()
        con.close()








