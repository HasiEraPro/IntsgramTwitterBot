from flask import Flask, render_template, request, url_for,redirect,flash
import os
from database import dbLite

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
            #if true there is a error,false if not
            status =  dbLite.adduser(instaName)
            print(status)
            if  not status == None:
                error = status
            else:
                flash('User added successfully')

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