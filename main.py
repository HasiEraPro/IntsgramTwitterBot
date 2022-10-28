import os
from time import sleep
from typing import Dict, List

from instagrapi import Client
from instagrapi.types import UserShort
from database.database import SqliteDB  as sql
import tweet

IG_USERNAME = 'pasindusamaranayake'
IG_PASSWORD = 'adalanane'
IG_CREDENTIAL_PATH = './ig_settings.json'
SLEEP_TIME = '600'  # in seconds


class Bot:
    _cl = None

    def __init__(self):
        self._cl = Client()
        if os.path.exists(IG_CREDENTIAL_PATH):
            self._cl.load_settings(IG_CREDENTIAL_PATH)
            self._cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            self._cl.login(IG_USERNAME, IG_PASSWORD)
            self._cl.dump_settings(IG_CREDENTIAL_PATH)

    def follow_by_username(self, username) -> bool:
        """
        Follow a user

        Parameters
        ----------
        username: str
            Username for an Instagram account

        Returns
        -------
        bool
            A boolean value is set
        """
        userid = self._cl.user_id_from_username(username)
        return self._cl.user_follow(userid)

    def unfollow_by_username(self, username) -> bool:
        """
        Unfollow a user

        Parameters
        ----------
        username: str
            Username for an Instagram account

        Returns
        -------
        bool
            A boolean value
        """
        userid = self._cl.user_id_from_username(username)
        return self._cl.user_unfollow(userid)

    def get_followers(self, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followers

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        Dict[int, UserShort]
            Dict of user_id and User object
        """
        return self._cl.user_followers(self._cl.user_id, amount=amount)

    def get_followers_usernames(self, amount: int = 0) -> List[str]:
        """
        Get bot's followers usernames

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        List[str]
            List of usernames
        """
        followers = self._cl.user_followers(self._cl.user_id, amount=amount)
        return [user.username for user in followers.values()]

    def get_following(self, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followed users

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        Dict[int, UserShort]
            Dict of user_id and User object
        """
        return self._cl.user_following(self._cl.user_id, amount=amount)

    def get_following_usernames(self, amount: int = 0) -> List[str]:
        """
        Get bot's followed usernames

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        List[str]
            List of usernames
        """
        following = self._cl.user_following(self._cl.user_id, amount=amount)
        print("following")
        return [user.username for user in following.values()]

    def update(self):
        """
        Do something
        """
        pass


def loop():
    # init db ,if db not initialised  initialise it
    dbLite = sql()

    # initialise bot
    cl = Client()
    cl.login("pasindusamaranayake", "crowmaster201")

    allusers = dbLite.getallusers()
    newUSer = False

    for user in allusers:

        #get the user id of the database using insta name
        userRowID = dbLite.getIdOfTheUser(user)

        #if user has no entry inside the database add user into the database
        if userRowID == None:
            dbLite.adduser(user)
            userRowID = dbLite.getIdOfTheUser(user)


        #get user id from instagram API
        instaAPIuserID = cl.user_id_from_username(user)

        #take all following people of the users using above instagram API
        followingActually = cl.user_following(instaAPIuserID, amount=7500)



        #if a new user user has no list of following inside the database,so we add all the following into db
        if newUSer:
            dbLite.addfollowers(followingActually,user)
            newUSer = False
            continue

        else:
            # take all the following people of the user inside db
            followinginDB = dbLite.getlistoffollowing(user)

            #what names inside database and dont have in the actual list
            unfollowedPerson = compareLists(followinginDB,followingActually)

            #names we have inside actual list which dont have inside database
            newfollowedPerson = compareLists(followingActually,followinginDB)



def compareLists(list1,list2):
    s = set(list2)
    temp3 = set(list1) - set(list2)
    print(temp3)
    return temp3

if __name__ == '__main__':
    # dbLite = sql()
    # result = dbLite.getlistoffollowing("instaId")
    # print(result)

    dblist = ["follower1","follower2","follower4"]
    actualList = ["follower3", "follower2"]

    # unfollowedPerson = compareLists(dblist,actualList)
    #
    # newfollowedPerson = compareLists(actualList,dblist)





    # bot = Bot()
    # user_id = bot.user_id_from_username("kimkardashian")
    # list = bot.get_following_usernames(user_id,100)
    # print (list)
    # print(len(list))  cvcvcv

    # cl = Client()
    # cl.login("pasindusamaranayake", "crowmaster201")
    #
    # user_id = cl.user_id_from_username("kimkardashian")
    #
    # print(user_id)
    # followers = cl.user_following(user_id, 7500)
    #
    # count =0
    # for user in followers.values():
    #     count+=1
    #     print(f"Number {count}:={user.username}")


