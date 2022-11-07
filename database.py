import sqlite3
from os.path import isfile

import config

class SqliteDB:

    def __init__(self):
        self.db_file = config.DB_FILE
        print(f"db file path = {self.db_file}")
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
               INSTA_NAME text,
               INSTA_ID text
           )''')
            print("Users Table Created")
            cur.execute('''CREATE TABLE following (
                       PERSON_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       INSTA_NAME text,
                       USER_ID INTEGER,
                       CONSTRAINT fk_users
                           FOREIGN KEY (USER_ID)
                           REFERENCES users(USER_ID)

                   )''')
            print("follwing persons table Created")

            cur.execute('''CREATE TABLE templates (
                                   TEMPL_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                   FOLLOW_TEXT text,
                                   FOLLOW_TEXT text,
                                   COMBINED_TEXT text

                               )''')
            cur.execute('''INSERT INTO templates (FOLLOW_TEXT,FOLLOW_TEXT) 
            VALUES 
            ("{user} has follwed the {followings}",
              "{user} has unfollowed the {unfollowings} "
              
            )''')
            print("template table Created")
        except Exception as e:
            print(f"Error in table creation:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()

    # add user into user table,we list the followers from this user
    def adduser(self, instaUserName,instaID):

        con = self.createDatabaseConnection()
        cur = con.cursor()
        error = None
        try:

            #check user is already there or not
            rowid = self.getIdOfTheUser(instaUserName)

            if not rowid == None:
                error = "user already here"
                print("user already in database")
                return


            sql = '''INSERT INTO users (INSTA_NAME,INSTA_ID) VALUES(?,?)'''
            cur.execute(sql, [instaUserName,instaID])
            print(f"Successfully added user:{instaUserName} insta ID {instaID}")
        except Exception as e:
            print(f"Coudnt insert user into db:={e}")
            error = "user not instagram"
        finally:
            con.commit()
            con.close()
            return error

    def addfollowers(self,followerList ,instauserName):

        userId = self.getIdOfTheUser(instauserName)

        con = self.createDatabaseConnection()
        cur = con.cursor()
        try:

            sql = '''INSERT INTO following (INSTA_NAME,USER_ID) VALUES(?,?)'''

            for follower in followerList:

                cur.execute(sql, [follower, userId])

            print(f"Successfully added {len(followerList)} of  following people")
        except Exception as e:
            print(f"Coudnt insert user into db:={e}")

        finally:
            con.commit()
            con.close()


    def getIdOfTheUser(self,instaName):
        con = self.createDatabaseConnection()
        cur = con.cursor()
        idFound = None
        id = None
        try:

            sql = f'SELECT USER_ID from users WHERE (INSTA_NAME=?)'

            idFound = cur.execute(sql,[instaName]).fetchone()

            if idFound is not None:

                id = idFound[0]
                print(f"User id of the {instaName} is {idFound[0]}")

            else:
                print(f"User id of {instaName} not found")

        except Exception as e:
            print(f"Exception Id not found:={e}")

        finally:
            con.commit()
            con.close()
            return id

    def getinstaIDofuser(self,instaName):
        con = self.createDatabaseConnection()
        cur = con.cursor()
        idFound = None
        id = None
        try:

            sql = f'SELECT INSTA_ID from users WHERE (INSTA_NAME=?)'

            idFound = cur.execute(sql, [instaName]).fetchone()

            if idFound is not None:

                id = idFound[0]
                print(f"insta id of the {instaName} is {idFound[0]}")

            else:

                print(f"Insta id of {instaName} not found")

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

            sql = f'SELECT INSTA_NAME from following WHERE (USER_ID=?)'

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

            sql = f'SELECT INSTA_NAME from users '

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

    def addTemplateText(self,followText = None, unfollowText=None,combinationtext=None):
        con = self.createDatabaseConnection()
        cur = con.cursor()
        print(f"i recived template data follow={followText} unfollow={unfollowText} combi={combinationtext}")
        try:
            sql = '''UPDATE templates SET FOLLOW_TEXT=?,UNFOLLOW_TEXT=?,COMBINED_TEXT=? WHERE TEMPL_ID=1'''
            cur.execute(sql, [followText,unfollowText,combinationtext])

            print(f"follow text:={followText} updated in db")
            print(f"unfollow text:={unfollowText} updated in db")
            print(f"combination text:={combinationtext} updated in db")



        except Exception as e:
            print(f"tweeter template text not added:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()

    def getFollowerTweetText(self):
        con = self.createDatabaseConnection()
        cur = con.cursor()
        text = ""
        try:
            sql = f'SELECT FOLLOW_TEXT from templates WHERE TEMPL_ID=1 '

            for row in cur.execute(sql).fetchall():
                text = row[0]

            print(f"found follwer tweet text = {text}")

        except Exception as e:
            print(f"Cant choose followers tweet text:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()
            return text

    def getunFollowerTweetText(self):
        con = self.createDatabaseConnection()
        cur = con.cursor()
        text = ""
        try:
            sql = f'SELECT UNFOLLOW_TEXT from templates WHERE TEMPL_ID=1 '

            for row in cur.execute(sql).fetchall():
                text = row[0]

            print(f"found unfollwer tweet text = {text}")

        except Exception as e:
            print(f"Cant choose unfollowers tweet text:={e}")

        finally:
            con.commit()
            cur.close()
            con.close()
            return text

    def createDatabaseConnection(self):

        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Exception as e:
            print(f"Databse connection failed:={e}")

        return conn


dbLite = SqliteDB()
