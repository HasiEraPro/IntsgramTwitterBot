from flask import Flask, render_template, request, url_for, redirect, flash, jsonify,Response
import sys
from instagrapi.exceptions import UserNotFound

#sys.path.append('/home/h4si/instaBot/IntsgramTwitterBot')
from database import dbLite
from insta import Bot

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#create the object here too ,because in gunicorn this app imports,so "if __name__" part not runs
#but in development its ok to have that above part

instaBot = Bot()

@app.route('/getFollowings')
def getfollowings():
    # take all following people of the users using above instagram API
    oncomingID = request.args.get('instaID',default=None,type=str)
    followingActually =[]
    status = ""
    print(f"oncomingID {oncomingID}")
    if oncomingID:
        try:

            followingActually = instaBot.get_following_usernames(oncomingID,7500)

            if len(followingActually) > 0:
                status = "ok"
            else:
                status = "no followings"

        except  Exception as e:
            print("error fetching following people of the user")
            status = "server exception"
        finally:
            return {"data": followingActually, "status": status}
    else:
        return {"data":followingActually, "status" : "empty request"}

@app.route('/',methods=('GET', 'POST'))
def home():
    error = None
    if request.method == "POST":

        instaName= request.form['instaName']
        followtxt = request.form['followTxt']
        unfollowTxt = request.form['unfollowTxt']


        print("submited requests-")
        print(f"follow txt:= {followtxt}")
        print(f"unfollow txt:= {unfollowTxt}")

        if (len(instaName) > 0):

            #check username is valid inside instagram
            instauserID = instaBot.is_user_valid(instaName)


            if(len(instauserID)  > 3):
                print("user is a valid user")
                try:

                    # if true there is a error,false if not
                    error = dbLite.adduser(instaName,instauserID)

                    if error == None:
                        flash('User added successfully')
                    else:
                        users = dbLite.getallusers()
                        return render_template('index.html', error=error, users=users)


                except Exception as e:
                    print(f"exception happens {e}")
            else:
                print(f"instagram user not found")
                error = "User not found on Instagram"
                users = dbLite.getallusers()
                return render_template('index.html', error=error, users=users)



        if not followtxt == "" and not unfollowTxt == "":
            dbLite.addTemplateText(followText=followtxt,unfollowText=unfollowTxt)
            flash('Follow and Unfollow text updated successfully')
        elif not followtxt == "":
            dbLite.addTemplateText(followText=followtxt,unfollowText=None)
            flash('Follow text updated successfully')
        elif not unfollowTxt == "":
            dbLite.addTemplateText(unfollowText=unfollowTxt)
            flash('Unfollow text updated successfully')

        users = dbLite.getallusers()
        return render_template('index.html', error=error, users=users)

    else:
        users = dbLite.getallusers()
        return  render_template('index.html',error=error,users=users)



#main driver function
if __name__ == '__main__':

    instaBot = Bot()
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(use_reloader=False)