"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, redirect, post
from datetime import datetime
from Connection import coll, games
from bson import ObjectId
import random
import uuid
from bottle import static_file
import os
import ast
import dis
import test

dis.dis(test)

@route('/')
@route('/home')
@view('index')
def home():
    return dict(
        hide="display: initial;",
        year=datetime.now().year
    )


@route('/Continue')
@view('index')
def home():
    



    return dict(
        year=datetime.now().year
    )

@route('/new')
@view('game')
def newGame():

    uWarDeck = []
    rWarDeck = []

    userName = request.query.get('txtName')

    suits = coll.distinct("Suits")
    rank = coll.distinct("Rank")
    randDeck = []
   

    while len(randDeck) < 52: #off the top of my head.. SHUFFLE!!!!!!
            randRank = random.randint(0,len(rank) -1)
            randSuit = random.randint(0,len(suits) -1)
            card = [suits[randSuit],rank[randRank]] #create random card
            if len(randDeck) == 0:#first card so we just add it
                randDeck.append(card)
            else:
                cardMatch = False;
                for c in randDeck: #checks if card exists
                    if c == card:
                        cardMatch = True
                        break
                if cardMatch == False:
                    randDeck.append(card)


    splitDeck = split(randDeck, 26)
    UserDeck = splitDeck[0]
    RoboDeck =  splitDeck[1]
    gameCode = uuid.uuid4().hex

    games.insert_one({ "gameCode": gameCode, "userName": userName, "roboDeck": RoboDeck, "userDeck":UserDeck })

    uWarDeck.append(UserDeck[0])
    rWarDeck.append(RoboDeck[0])

    return dict(
        userScore = 0,
        roboScore = 0,
        user =userName,
        code = gameCode,
        userCards = uWarDeck,
        roboCards = rWarDeck,
        year=datetime.now().year
    )

@route('/game/<ucard>/<robocard>/<gCode>')
@view('game')
def playGame(ucard, robocard, gCode): 

    uWarDeck = []
    rWarDeck = []

    #parse returned cards back into list objects
    rCard = ast.literal_eval(robocard)
    uCard = ast.literal_eval(ucard)

    #check if incoming round is a war
    if len(rCard) > 1:
        #get value of last cards
        rVal = CardValue(rCard[3])
        uVal = CardValue(uCard[3])

    else:
        #get card values
        
        rVal = CardValue(rCard[0])
        uVal = CardValue(uCard[0])


    #get decks from database
    UserDeck = list(games.find({"gameCode":gCode},{"userDeck":1,"_id":0}))[0]['userDeck']

    RoboDeck = list(games.find({"gameCode":gCode},{"roboDeck":1,"_id":0}))[0]['roboDeck']

    #Dont take away first two cards if a war is going to happen or if a war happens
    if uVal != rVal and len(rCard) < 2:
        games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )
        games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )
   
    #whoever wins round gets cards, if both cards equal a war begins
    if uVal > rVal:
        for c in uCard:
            games.update({"gameCode":gCode },{"$push":{"userDeck":c}})
        for c in rCard:
            games.update({"gameCode":gCode },{"$push":{"userDeck":c}})
        
        uWarDeck.append(UserDeck[0])
        rWarDeck.append(RoboDeck[0])

    elif uVal < rVal:
        for c in rCard:
            games.update({"gameCode":gCode },{"$push":{"roboDeck":c}})
        for c in uCard:
            games.update({"gameCode":gCode },{"$push":{"roboDeck":c}})
        
        uWarDeck.append(UserDeck[0])
        rWarDeck.append(RoboDeck[0])
    else:
        for x in range(4):
            uWarDeck.append(list(games.find({"gameCode":gCode},{"userDeck":1,"_id":0}))[0]['userDeck'][0])
            games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )
            rWarDeck.append(list(games.find({"gameCode":gCode},{"roboDeck":1,"_id":0}))[0]['roboDeck'][0])
            games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )
    
            
    UserDeck = list(games.find({"gameCode":gCode},{"userDeck":1,"_id":0}))[0]['userDeck']
    userDeckLen = len(UserDeck)

    RoboDeck = list(games.find({"gameCode":gCode},{"roboDeck":1,"_id":0}))[0]['roboDeck']
    roboDeckLen = len(RoboDeck)
            
            

         

    userName = games.distinct("userName",{"gameCode":gCode})[0]


    return dict(
        userScore = userDeckLen,
        roboScore = roboDeckLen,
        user =userName,
        code = gCode,
        userCards = uWarDeck,
        roboCards = rWarDeck,
        year=datetime.now().year
    )


@route('/static/<filepath:path>')
def server_static(filepath):
     myPath = os.path.join(os.getcwd(), "static") #join current directory to static folder as a full path
     return static_file(filename, root=myPath)

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

def CardValue(card):
    c = card[1]
    if c == "K" or c == "J" or c =="Q":
        return 10
    elif c == "A":
        return 11
    else:
        return int(c)
