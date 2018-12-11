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
   

    while len(randDeck) < 52: 
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


@route('/gameOver/<winner>')
@view('gameOver')
def gameOver(winner):

    return dict(
        year=datetime.now().year,
        winner = winner
        )


@route('/game/<ucard>/<robocard>/<gCode>')
@view('game')
def playGame(ucard, robocard, gCode): 



    uWarDeck = []
    rWarDeck = []

    #parse returned cards back into list objects
    rCard = ast.literal_eval(robocard)
    uCard = ast.literal_eval(ucard)

    #get last card in list val, this will handle if it is a war game or a single card
    rVal = CardValue(rCard[len(rCard) - 1])
    uVal = CardValue(uCard[len(uCard) - 1])

    #each user will always have the same ammount of cards on deck so we can just get the count from one of the decks
    onDeckCount = len(rCard)


    #get decks from database
    UserDeck = list(games.find({"gameCode":gCode},{"userDeck":1,"_id":0}))[0]['userDeck']
    userDeckLen = len(UserDeck)

    RoboDeck = list(games.find({"gameCode":gCode},{"roboDeck":1,"_id":0}))[0]['roboDeck']
    roboDeckLen = len(RoboDeck)

    if userDeckLen >= 52:
        redirect("/gameOver/User")
    elif roboDeckLen >=52:
        redirect("/gameOver/Robo") 

   
    #whoever wins round gets cards, if both cards equal a war begins
    if uVal > rVal:
        for x in range(onDeckCount):
            #add won cards to user
            games.update({"gameCode":gCode },{"$push":{"userDeck":rCard[x]}})
            games.update({"gameCode":gCode },{"$push":{"userDeck":uCard[x]}})
            #remove lost cards from Robo, also move existing cards to rear
            if len(uCard) < 2 and uVal > rVal:
                games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )
                games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )

        #set up next hand
        uWarDeck.append(UserDeck[1])
        rWarDeck.append(RoboDeck[1])

    elif uVal < rVal:
        for x in range(onDeckCount):
            games.update({"gameCode":gCode },{"$push":{"roboDeck":rCard[x]}})
            games.update({"gameCode":gCode },{"$push":{"roboDeck":uCard[x]}})
            #remove lost cards from User, also move existing cards to rear
            if len(rCard) <2 and uVal < rVal:
                games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )
                games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )

        #set up next hand
        uWarDeck.append(UserDeck[1])
        rWarDeck.append(RoboDeck[1])
            
    else:
        #add existing cards to war game + 4 because final card matches
        for x in range(onDeckCount):
            uWarDeck.append(uCard[x])
            rWarDeck.append(rCard[x])
        for x in range(4):
            games.update({"gameCode":gCode }, { "$pop": { "userDeck": -1 } } )
            uWarDeck.append(list(games.find({"gameCode":gCode},{"userDeck":1,"_id":0}))[0]['userDeck'][0])
            games.update({"gameCode":gCode }, { "$pop": { "roboDeck": -1 } } )
            rWarDeck.append(list(games.find({"gameCode":gCode},{"roboDeck":1,"_id":0}))[0]['roboDeck'][0])
            
    
            
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


