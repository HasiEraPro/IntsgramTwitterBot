from database.database import dbLite
from insta import cl
import tweet


def loop():

    allusers = dbLite.getallusers()
    print(f"there are {len(allusers)} users in db")

    for user in allusers:

        #get the user id of the database using insta name
        userRowID = dbLite.getIdOfTheUser(user)

        try:
            #get user id from instagram API
            instaAPIuserID = cl.user_id_from_username(user)
        except Exception as e:
            print(f"insta ID not found of the user {user}")
            continue

        # take all the following people of the user inside db
        followinginDB = dbLite.getlistoffollowing(user)

        #take all following people of the users using above instagram API
        tempInstaDic = cl.user_following(instaAPIuserID, amount=7500)

        #extract user names from actualFollowingLists
        followingActually = [user.username for user in tempInstaDic.values()]


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
            if len(newfollowedPerson) > 0 and len(unfollowedPerson) == 0:

                print(f"user {user} has new followings,starting tweets")
                #tweet follows people
                tweet.tweetFollow(user,newfollowedPerson)
                print(f"tweeting Ends")

            #if unfollwed and followed has been done
            elif len(newfollowedPerson) > 0 and len(unfollowedPerson) > 0:
                print(f"user {user} has new followings and unfollowings,starting tweets")
                followedString = ",".join(["@"+x for x in newfollowedPerson])
                unfollowedString = ",".join(["@"+x for x in unfollowedPerson])

                message = f"{user} has followed {followedString} and unfollowed {unfollowedString}"
                print(f"tweeting this message {message}")
                tweet.tweetMessage(message)
                print(f"tweeting Ends")

            #if only new unfollowers are their
            elif len(newfollowedPerson) == 0 and len(unfollowedPerson) > 0:
                print(f"user {user} has unfollowings,start tweeting")
                # tweet unfollows people
                tweet.tweetUnFollow(user, unfollowedPerson)

                print(f"tweeting Ends")




def compareLists(list1,list2):

    temp3 = set(list1) - set(list2)
    print(temp3)
    return temp3

if __name__ == '__main__':

    loop()

    #old code
    """
    # result = dbLite.getlistoffollowing("instaId")
    # print(result)

    # dblist = ["follower1","follower2","follower4"]
    # actualList = ["follower3", "follower2"]

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
    #user_id = cl.user_id_from_username("kimkardashian")
    #
    # print(user_id)
    #followers = cl.user_following(user_id, 10)

   # print([user.username for user in followers.values()])
    #
    # count =0
    # for user in followers.values():
    #     count+=1
    #     print(f"Number {count}:={user.username}")
    """

