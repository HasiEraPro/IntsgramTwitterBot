import sqlite3


class SqliteDB:

    def __init__(self):
        # Database
        con = sqlite3.connect('instagram.db')
        cur = con.cursor()
        try:
            cur.execute('''CREATE TABLE users (
                USER_ID INTEGER PRIMARY KEY INCREMENT,
                NAME text,
                INSTA_ID text, 
            )''')
            print("Users Table Created")
            cur.execute('''CREATE TABLE following (
                        PERSON_ID INTEGER PRIMARY KEY INCREMENT,
                        NAME text,
                        INSTA_ID text,
                        CONSTRAINT fk_departments
                            FOREIGN KEY (USER_id)
                            REFERENCES users(USER_ID)
                         
                    )''')
            print("follwing persons table Created")

        except Exception as e:
            print(f"Error in table creation:={e}")

        con.commit()
        con.close()


#database instance
db = SqliteDB()






