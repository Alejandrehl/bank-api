from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.bankapi
users = db["users"]

def userExist(username):
    if users.find({"username": username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if userExist(username):
            retJson = {
                "status" : 301,
                "msg" : "Invalid username"
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert({
            "username" : username,
            "password" : hashed_pw,
            "own" : 0,
            "debt" : 0,
        })

        retJson = {
            "status" : 200,
            "msg" : "You succesfully signed up for the API"
        }

        return jsonify(retJson)

def verifyPw(username, password):
    if not userExist(username):
        return False
    
    hashed_pw = users.find({
        "username" : username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def cashWithUser(username):
    cash = users.find({
        "username" : username
    })[0]["own"]
    return cash

def debtWithUser(username):
    debt = users.find({
        "username" : username
    })[0]["debt"]
    return debt

def generateReturnDictionary(status, msg):
    retJson = {
        "status" : status,
        "msg" : msg
    }
    return retJson

def verifyCredentials(username, password):
    if not userExist(username):
        return generateReturnDictionary(301, "Invalid username"), True
    
    correct_pw = verifyPw(username, password)
    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True
    
    return None, False

def updateAccount(username, balance):
    users.update({
        "username" : username
    }, {
        "$set" : {
            "own" : balance
        }
    })

def updateDebt(username, balance):
    users.update({
        "username" : username
    }, {
        "$set" : {
            "debt" : balance
        }
    })

class Add(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        if money <= 0:
            return jsonify(generateReturnDictionary(304, "The money amount entered must be > 0"))
        
        cash = cashWithUser(username)
        money -= 1
        bank_cash = cashWithUser("BANK")
        updateAccount("BANK", bank_cash + 1)
        updateAccount(username, cash + money)

        return jsonify(generateReturnDictionary(200, "Amount added succesfully to account."))

class Transfer(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error: 
            return jsonify(retJson)

        cash = cashWithUser(username)
        if cash <= 0:
            return jsonify(generateReturnDictionary(304, "You're out of money."))
        
        if not userExist(to):
            return jsonify(301, "Reciever username is invalid.")
        
        cash_from = cashWithUser(username)
        cash_to = cashWithUser(to)
        bank_cash = cashWithUser("BANK")

        updateAccount("BANK", bank_cash+1)
        updateAccount(to, cash_to + money - 1)
        updateAccount(username, cash_from - money)

        return jsonify(generateReturnDictionary(200, "Amount transfered sucessfully."))

        

    



