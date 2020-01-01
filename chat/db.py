from pymongo import MongoClient


def db_conn():
	db_client = MongoClient('localhost', 27017)
	db = db_client.kodesmil
	return db
