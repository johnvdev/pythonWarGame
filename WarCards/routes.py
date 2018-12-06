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

    userName = request.query.get('txtName')

    suits = coll.distinct("Suits")
    rank = coll.distinct("Rank")
    randDeck = []
   

    while len(randDeck) < 52: #off the top of my head.. SHUFFLE!!!!!!
            randRank = random.randint(0,len(rank) -1)
            randSuit = random.randint(0,len(suits) -1)
            card = [suits[randSuit],rank[randRank], randRank +1] #create random card
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
        userScore = 0,
        roboScore = 0,
        user =userName,
        code = gameCode,
        userCard = UserDeck[0],
        roboCard = RoboDeck[0],
        year=datetime.now().year
    )

@route('/game/<ucard>/<robocard>/<gCode>')
@view('game')
def playGame(ucard, robocard, gCode): 

    rCard = ast.literal_eval(robocard)
    uCard = ast.literal_eval(ucard)

    rCardVal = rCard[2]
    uCardVal = uCard[2]

    UserDeck = games.distinct("userDeck",{"gameCode":gCode})
    userDeckLen = len(list(UserDeck))

    RoboDeck = games.distinct("roboDeck",{"gameCode":gCode})
    roboDeckLen = len(list(RoboDeck))

    if uCardVal > rCardVal:
         games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )
         games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )

    elif uCardVal < rCardVal:
          games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )
          games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )


    UserDeck = games.distinct("userDeck",{"gameCode":gCode})
    userDeckLen = len(list(UserDeck))

    RoboDeck = games.distinct("roboDeck",{"gameCode":gCode})
    roboDeckLen = len(list(RoboDeck))

    userName = games.distinct("userName",{"gameCode":gCode})[0]


    return dict(
        userScore = 0,
        roboScore = 0,
        user =userName,
        code = gCode,
        userCard = UserDeck[0],
        roboCard = RoboDeck[0],
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