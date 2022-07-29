
from flask import Flask,  request, Response,jsonify
from flask_pymongo import PyMongo
import json


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/books")
books = mongo.db.books

import crud


@app.route("/",methods=['GET'])
def home():
    return "Welcome :)"


@app.route("/get", methods = ["GET"])
def get_all_book():
    return crud.Get_All_Books()
    
    

@app.route('/add', methods = ['POST'])
def add_book():
    return crud.Add_Book()

@app.route('/search_by_term',methods= ['GET'])
def search_by_term():
	# response = crud.Search_By_Name(name)
	# return jsonify({"message":"success","response":f"{response}"})
    return crud.Search_By_Term()

@app.route("/get_by_name/<string:name>",methods = ['GET'])
def get_book(name):
    return crud.Get_By_Name(name)

@app.route("/books_within_rent_price_range",methods = ["GET"])
def books_within_rent_price_range():
    return crud.Books_Within_Rent_Price_Range()

@app.route("/search",methods = ["GET"])
def search():
    return crud.Search()


#######################################################################################################

mongo1 = PyMongo(app, uri="mongodb://localhost:27017/booksTransactions")
transaction = mongo.db.booksTransactions

@app.route("/book_issue",methods = ['POST'])
def book_issue():
    return crud.Book_Issue()


@app.route("/return_book",methods = ['PUT'])
def return_book():
    return crud.Return_Book()

#########################################################################################################################################

@app.route("/person_who_taken_book",methods=['POST'])
def person_who_taken_book():
    return crud.Person_Who_Taken_Book()
    

@app.route("/book_taken_by_person",methods=["POST"])
def book_taken_by_person():
    return crud.Book_Taken_By_Person()

@app.route("/total_rent_generated_by_book",methods = ['GET'])
def total_rent_generated_by_book():
    return crud.Total_Rent_Generated_By_Book()
    

@app.route("/book_issue_between_date",methods=["POST"])
def book_issue_between_date():
    return crud.Book_Issue_Between_Date()
    



# driver function
if __name__ == '__main__':
	app.run(port=9000,debug = True)
