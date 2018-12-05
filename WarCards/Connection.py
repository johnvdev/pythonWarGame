from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
db = conn.final_project
coll = db.deck
games = db.games

