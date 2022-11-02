from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
import sys
from instagrapi.exceptions import UserNotFound

#sys.path.append('/home/h4si/instaBot/IntsgramTwitterBot')
from database import dbLite
from insta import cl

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/getFollowings')
def getfollowings():
    # take all following people of the users using above instagram API
    oncomingID = request.args.get('instaID',default=None,type=str)
    followingActually =[]
    print(f"oncomingID {oncomingID}")
    if oncomingID:
        try:
            #tempInstaDic = cl.user_following(oncomingID, amount=7500)
            #followingActually = [user.username for user in tempInstaDic.values()]
            followingActually =["fol1","fol2","fol3"]
            return jsonify({"data":followingActually,"error":"None"})

        except  Exception as e:
            print("error fetching following people of the user")
            return jsonify({"data":"None","error":e})

    else:
        return jsonify({"data": "None", "error": "empty request"})

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
            try:
                instauserID = cl.user_id_from_username(instaName)
                # if true there is a error,false if not
                error = dbLite.adduser(instaName,instauserID)

                if error == None:
                    flash('User added successfully')
                else:
                    users = dbLite.getallusers()
                    return render_template('index.html', error=error, users=users)


            except UserNotFound as e:
                print(f"instagram user not found")
                error = "User not found on Instagram"
                users = dbLite.getallusers()
                return render_template('index.html', error=error, users=users)

            except Exception as e:

                print(f"exception happens {e}")



        if not followtxt == "" and not unfollowTxt == "":
            dbLite.addTemplateText(followText=followtxt,unfollowText=unfollowTxt)
        elif not followtxt == "":
            dbLite.addTemplateText(followText=followtxt,unfollowText=None)
        elif not unfollowTxt == "":
            dbLite.addTemplateText(unfollowText=unfollowTxt)

        users = dbLite.getallusers()
        return render_template('index.html', error=error, users=users)

    else:
        users = dbLite.getallusers()
        return  render_template('index.html',error=error,users=users)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()