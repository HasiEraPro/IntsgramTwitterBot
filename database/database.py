import sqlite3
from os.path import isfile
from insta import cl

class SqliteDB:

    def __init__(self):
        self.db_file = r'database/instagram.db'

        # this runs at first time of the db creation
        if not isfile(self.db_file):
            self.firsttimerun()


    def firsttimerun(self):
        # Database connection
        con = self.createDatabaseConnection()
        cur = con.cursor()
        print("First time run Database")
        try:

            cur.execute('''CREATE TABLE users (
               USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               INSTA_ID text
           )''')
            print("Users Table Created")
            cur.execute('''CREATE TABLE following (
                       PERSON_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       INSTA_ID text,
                       USER_ID INTEGER,
                       CONSTRAINT fk_users
                           FOREIGN KEY (USER_ID)
                           REFERENCES users(USER_ID)

                   )''')
            print("follwing persons table Created")

        except Exception as e:
            print(f"Error in table creation:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()

    # add user into user table,we list the followers from this user
    def adduser(self, instaUserName):

        con = self.createDatabaseConnection()
        cur = con.cursor()
        error = False
        try:
            #check the given username is valid in instagram
            print(f"user {instaUserName} is valid ID:={cl.user_id_from_username(instaUserName)}")

            sql = '''INSERT INTO users (INSTA_ID) VALUES(?)'''
            cur.execute(sql, [instaUserName])
            print(f"Successfully added user:{instaUserName}")
        except Exception as e:
            print(f"Coudnt insert user into db:={e}")
            error = True
        finally:
            con.commit()
            con.close()
            return error

    def addfollowers(self,followerList ,instauserName):

        userId = self.getIdOfTheUser(instauserName)

        con = self.createDatabaseConnection()
        cur = con.cursor()
        try:

            sql = '''INSERT INTO following (INSTA_ID,USER_ID) VALUES(?,?)'''

            for follower in followerList:

                cur.execute(sql, [follower, userId])

            print(f"Successfully added {len(followerList)} of  following people")
        except Exception as e:
            print(f"Coudnt insert user into db:={e}")

        finally:
            con.commit()
            con.close()


    def getIdOfTheUser(self,instaID):
        con = self.createDatabaseConnection()
        cur = con.cursor()
        idFound = None
        id = None
        try:

            sql = f'SELECT USER_ID from users WHERE (INSTA_ID=?)'

            idFound = cur.execute(sql,[instaID]).fetchone()

            if idFound is not None:

                id = idFound[0]
                print(f"User id of the {instaID} is {idFound[0]}")

            else:
                print(f"User id of {instaID} not found")

        except Exception as e:
            print(f"Exception Id not found:={e}")

        finally:
            con.commit()
            con.close()
            return id
    
    def getlistoffollowing(self,userinstaName):

        userId = self.getIdOfTheUser(userinstaName)
        con = self.createDatabaseConnection()
        cur = con.cursor()
        followingList = []
        try:

            sql = f'SELECT INSTA_ID from following WHERE (USER_ID=?)'

            result = cur.execute(sql, [userId]).fetchall()

            print(f"{len(result)} number of following found of user {userinstaName}")

            if result is not None:

                if len(result) > 0:
                    for item in result:
                        followingList.append(item[0])

                    print(f"there are {len(followingList)} of following inside db of user {userinstaName}")
                else:
                    print(f"following list is empty or  no following")

            else:
                print(f"something wrong with the following table")


        except Exception as e:
            print(f"following people not found:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()
            return followingList

    def getallusers(self):

        con = self.createDatabaseConnection()
        cur = con.cursor()
        fullUserList = []

        try:

            sql = f'SELECT INSTA_ID from users '

            for row in cur.execute(sql).fetchall():
                fullUserList.append(row[0])

            print(f"there are {len(fullUserList) } of users inside db")

        except Exception as e:
            print(f"following people not found:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()
            return fullUserList

    def createDatabaseConnection(self):

        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Exception as e:
            print(f"Databse connection failed:={e}")

        return conn


dbLite = SqliteDB()
