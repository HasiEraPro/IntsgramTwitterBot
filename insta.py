import os
import time
from typing import Dict, List
from instagrapi import Client
from instagrapi.types import UserShort
from instagrapi.exceptions import *

import config

SLEEP_TIME = '600'  # in seconds


class Bot:
    _cl = None

    def __init__(self):
        self._cl = Client()
        print(f"iq settings file in {config.IG_CREDENTIAL_PATH}  {os.path.exists(config.IG_CREDENTIAL_PATH)}")
        if os.path.exists(config.IG_CREDENTIAL_PATH):
            print("insta bot using ig settings file")
            self._cl.load_settings(config.IG_CREDENTIAL_PATH)
            self._cl.login(config.IG_USERNAME, config.IG_PASSWORD)

        else:
            print("insta bot using name and password")
            self._cl.login(config.IG_USERNAME, config.IG_PASSWORD)
            self._cl.dump_settings(config.IG_CREDENTIAL_PATH)

    def is_user_valid(self,username) -> str:
        result = "0"
        try:
            userid = self._cl.user_id_from_username(username)
            result = userid
        except Exception as e:
            print(f"[instaBot]>user not found in instagram:={e}")
        finally:
            return result

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

    def get_followers(self, userID:str ,amount: int = 0) -> Dict[str, UserShort]:
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
        return self._cl.user_followers(userID, amount=amount)

    def get_followers_usernames(self,userID:str,amount: int = 0) -> List[str]:
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
        followers = self._cl.user_followers(userID, amount=amount)
        return [user.username for user in followers.values()]

    def get_following(self, userID:str,amount: int = 0) -> Dict[str, UserShort]:
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
        return self._cl.user_following(userID, amount=amount)

    def get_following_usernames(self, userID:str , amount: int = 0) -> List[str]:
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

        try:
            following = self._cl.user_following(userID, amount=amount)
            return [user.username for user in following.values()]

        except Exception as e:
            print(f"insta following module:={e}")
            return []

    def update(self):
        """
        Do something
        """
        pass

