"""Flask App Project."""

from flask import Flask, jsonify, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time

cred = credentials.Certificate('templates/PATH_TO_FIREBASE.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jaden-drone.firebaseio.com'
})
#Authenticate firebase

numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def onlyNumbs(inString):
    returnStr = ""
    for x in inString:
        if x in numList:
            returnStr += x
    return returnStr
# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/objRef')
ref2 = db.reference('/numberRef')
ref3 = db.reference('/sentRef')
ref4 = db.reference('/armPos')
app = Flask(__name__)

class storeClass:
    def __init__(self):
        self.x = ""

globs = storeClass()

chList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

@app.route('/')
def index():
    mnsr = ref.get()
    print(mnsr)
    return redirect(url_for('logs'))


@app.route('/<numbString>/posM')
def posM(numbString):
    print(numbString)
    ref4.set(numbString)
    revs = ref4.get()
    return str(revs)
    
@app.route('/getPos')
def getPos():
    revs = ref4.get()
    return str(revs)

if __name__ == '__main__':
    app.run()
