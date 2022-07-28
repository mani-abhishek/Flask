
from operator import le
from main import request,books,Response,json,app,jsonify,transaction
import utils
from datetime import date,datetime

def Home():
	if(request.method == 'GET'):

		data = "hello world"
		return jsonify({'data': data})


def Get_All_Books():
    result = list(books.find())
    response = app.response_class(
        response=json.dumps(result,default=str),
        status=200,
        mimetype='application/json'
    )
    return response

def Add_Book():
    # book = {'book_name':'Data Structure using JAVA','category':'Data Structure','rent_per_day':50}# Adding book Manually
    book_name = request.json['book_name']
    category = request.json['category']
    rent_per_day = request.json['rent_per_day']
    books.insert_one({"book_name":book_name,"category":category,"rent_per_day":rent_per_day})
    
    return jsonify({"Book Name ":book_name,"Category":category,"Rent/Day":rent_per_day})

def Get_By_Name(name):
    result = list(books.find({"book_name":{"$regex":name,'$options' : 'i'}}))
    return utils.response(result)

def Search_By_Term():
    result = list()
    # result = list(books.find({"book_name":{"$regex":name,'$options' : 'i'}}))
    for i in books.find({"book_name":{"$regex":request.args.get('name'),'$options' : 'i'}}):
        result.append({'Name':i['book_name'],'Category':i['category'],'Rent/Day':f"Rs.{i['rent_per_day']}"})
    # return json.dumps(result, default=str)
    return utils.response(result)
    # return Response(
    #    response =  json.dumps(result, default=str),
    #    mimetype="application/json",
    #    status=200
    # )
    
   
def Books_Within_Rent_Price_Range():
    result = list()
    min = int(request.args.get("min"))
    max = int(request.args.get("max"))
    book = list(books.find({'rent_per_day': { '$gte': min, '$lte': max}})) 
    for i in book:
        result.append({'Name':i['book_name'],'Category':i['category'],'Rent/Day':f"Rs.{i['rent_per_day']}"})
    
    return utils.response(result)

def Search():
    result = list()
    name = request.args.get("name")
    category = request.args.get("category")
    min = int(request.args.get("min"))
    max = int(request.args.get("max"))
    print(name,category,min,max)
    book = list(books.find({'$and':[{'book_name':{'$regex':name,'$options':'i'}},
                               {'category':{'$regex':category,'$options':'i'}},
                               {'rent_per_day':{'$gt':min,'$lt':max}}
    ]}))

    for i in book:
        result.append({'Name':i['book_name'],'Category':i['category'],'Rent/Day':f"Rs.{i['rent_per_day']}"})
    
    return utils.response(result)

# #######################################################################################################################
def Book_Issue():
    name = request.json['book_name']
    if(not books.find_one({"book_name":{'$regex':f"^{name}$",'$options' : 'i'}})):
        return utils.error("Book Not Found")
    
    issued_person = request.json['issued_person']

    if(transaction.find_one({"book_name":{'$regex':f"^{name}$",'$options' : 'i'},
                            "issued_person":{'$regex':f"^{issued_person}$",'$options':'i'},
                            "return_date":{'$exists':False}})):
        return utils.error("Please first return this before Reissue")

    issue_date = datetime.today().replace(microsecond=0)

    transaction.insert_one({"book_name":name,"issued_person":issued_person,"issue_date": issue_date})
    return jsonify({"message":"BOOK IS ISSUED","book_name":name,"issued_person":issued_person,"issue_date":issue_date})


def Return_Book():
    name = request.json['book_name']
    issued_person = request.json['issued_person']
    return_date = datetime.today().replace(microsecond=0)
    
    book = books.find_one({"book_name":{'$regex':f"^{name}$",'$options' : 'i'}})
    rent_per_day = book['rent_per_day']
    t = transaction.find_one({"book_name":{'$regex':f"^{name}$",'$options' : 'i'}})
    issue_date = t['issue_date']
    
    
    date_format = "%Y-%m-%d %H:%M:%S"
    a = datetime.strptime(str(issue_date), date_format)
    b = datetime.strptime(str(return_date), date_format)
    delta = b - a
    total_rent = rent_per_day if delta.days==0 else delta.days*rent_per_day
    transaction.update_one({'book_name':{'$regex':f"^{name}$",'$options':'i'},'issued_person':issued_person},{"$set":{"return_date": return_date,'total_rent':total_rent}})
    return jsonify({"message":{"":"Your Book is successfully returned","Total rent ": total_rent},"Boook Name ":name,"Your Name":issued_person})
    


########################################################################################################################################

def Person_Who_Taken_Book():
    old_issued = list()
    current_issued = list()
    name = request.json['book_name']
    t = list(transaction.find({"book_name":{"$regex":f"^{name}$",'$options' : 'i'},"return_date":{'$exists':True}}))
    for i in t:
        old_issued.append(i['issued_person'])
    t1 = list(transaction.find({"book_name":{"$regex":f"^{name}$",'$options' : 'i'},"return_date":{'$exists':False}}))
    for i in t1:
        current_issued.append(i['issued_person'])

    print(old_issued,len(t))
    print(current_issued,len(t1))

    return jsonify({f"List of people who have issued {name}= ":old_issued,f"List of people who currently have {name} book issued":current_issued })


def Total_Rent_Generated_By_Book():
    name = request.json['book_name']
    t = list(transaction.find({"book_name":{"$regex":f"^{name}$","$options" : 'i'},"return_date":{"$exists":"true"}}))
    # t = list(transaction.find({"book_name":{"$regex":f"^{name}$",'$options' : 'i'},"return_date":{'$exists':'true'}}))
    rent=0
    for i in t:
        rent=rent+i['rent']

    
    return "Success"

def Book_Taken_By_Person():
    person = list()
    person_name = request.json['person_name']

    t = list(transaction.find({"issued_person":{"$regex":f"^{person_name}$","$options":'i'}}))
    print(len(t))
    for i in t:
        person.append(i['issued_person'])
    
    print(person)

    return "Success"

def Book_Issue_Between_Date():
    d1 = request.args.get("date1")
    d2 = request.args.get("date2")
    print(d1,d2)


    return "Suscces"