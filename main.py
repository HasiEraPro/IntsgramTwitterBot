
from database import dbLite
import requests
import tweet
import config

def loop():

    allusers = dbLite.getallusers()
    print(f"there are {len(allusers)} users in db")

    for user in allusers:

        #get the user id of the database using insta name
        userRowID = dbLite.getIdOfTheUser(user)


        # get user id from instagram API
        instaAPIuserID = dbLite.getinstaIDofuser(user)

        # take all the following people of the user inside db
        followinginDB = dbLite.getlistoffollowing(user)

       #get followings from our API
        query = {'instaID': instaAPIuserID}
        response = requests.get(config.OUR_API_SERVER_FOLLOWINGS_END, params=query)
        print(f"response from API :- {response}")
        followingActually = response.json()["data"]
        error = response.json()["status"]
        print(f"API following fetch status:{error}")
        print(f"following list from API:={followingActually}")

        #if some user has no records of follwing inside the db
        if len(followinginDB) == 0:
            # if he actually dont have followings,dont do anything just pass
            if len(followingActually) == 0:
                print(f"user {user} dont follow anyone,skipping ")
                continue

            #check his instagram has followings,if it is add all the follwoings to db and goto next user
            if len(followingActually) > 0:

                dbLite.addfollowers(followingActually,user)
                print(f"new user {user} found...added {len(followingActually)} following into db ")
                continue



        else:


            #what names inside database and dont have in the actual list
            unfollowedPerson = compareLists(followinginDB,followingActually)
            print(f"user {user} has unfollowed these persons {unfollowedPerson}")

            #names we have inside actual list which dont have inside database
            newfollowedPerson = compareLists(followingActually,followinginDB)

            print(f"user {user} has followed these persons {newfollowedPerson}")
            #if only new follwers are there
            if len(newfollowedPerson) > 0 :
                followedString = ",".join(["@" + x for x in newfollowedPerson])
                print(f"user {user} has new followings,starting tweets")
                dbFollowingTxt = dbLite.getFollowerTweetText()

                #replace all the occurences of users

                replacedVersion1 = dbFollowingTxt.replace("{user}",user)

                # replace all followings

                replacedVersion2 = replacedVersion1.replace("{followings}", followedString)


                #tweet follows people
                tweet.tweetMessage(replacedVersion2)


            #if only new unfollowers are their
            elif len(unfollowedPerson) > 0:
                print(f"user {user} has unfollowings,start tweeting")

                # create a string of all unfollowed peoples
                unfollowedString = ",".join(["@"+x for x in unfollowedPerson])



                #get unfollower tweet message from db
                dbunFollowingTxt = dbLite.getunFollowerTweetText()

                # replace all the occurences of users

                replacedVersion1 = dbunFollowingTxt.replace("{user}", user)

                # replace all followings

                replacedVersion2 = replacedVersion1.replace("{unfollowings}", unfollowedString)


                # tweet unfollows people

                tweet.tweetMessage(replacedVersion2)

                print(f"tweeting Ends")




def compareLists(list1,list2):

    temp3 = set(list1) - set(list2)
    print(temp3)
    return temp3

if __name__ == '__main__':

    loop()



