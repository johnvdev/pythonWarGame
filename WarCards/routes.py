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

    return dict(
        user =userName,
        code = gameCode,
        userCard = UserDeck,
        roboCard = RoboDeck,
        year=datetime.now().year
    )

@route('/game/<ucard>/<robocard>/<gCode>')
@view('game')
def playGame(ucard, robocard, gCode): 

    if ucard[0][1] > robocard[0][1]:
         games.update({"code":gCode },{ "$pull": { "roboDeck": { "$in": robocard[0]}}},{ "multi": "false" })
         games.update({"code":gCode},{"$push":robocard[0]})


    return dict(
        user =userName,
        code = gameCode,
        userCardFace = UserDeck[0][0],
         userCardValue = UserDeck[0][1],
        roboCardFace = RoboDeck[0][0],
        roboCardValue = RoboDeck[0][1],
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