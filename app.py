from pymongo import MongoClient
from bson import ObjectId
import pprint

# -------------------------
# Database connection
# -------------------------
client = MongoClient("mongodb+srv://TechTitans_db_user:hello@techtitanssocialmediadb.nhwgwlf.mongodb.net/?retryWrites=true&w=majority&appName=TechTitansSocialMediaDB" )  # adjust if using Atlas
db = client["social_media_db"]      # replace with your chosen DB name
users = db["users"]    # example collection
posts = db["posts"]

pp = pprint.PrettyPrinter(indent=2)


# -------------------------
# CRUD Function Templates
# -------------------------

#function which uses MongoDB's insert query (only inserts 1 document)
def create_document(doc):
   db.users.insert_one(doc)

#function which uses MongoDB's insert many query
def create_many(doc):
    db.users.insert_many(doc)

#function which updates many documents given using multiple user inputs
def update_document():
    condition = {}
    not_done = True
    while not_done:#loop which causes user to input all the field they want to be checked
        field = input("Enter the field name you want to check: ")
        value = input("Enter the value for the key: ")
        condition.update({field:value})
        not_done = bool(int(input("Done?: Enter 0 for yes: ")))
        print(not_done)

    field_change = input("Enter the field you want to change: ")
    value_change = input("Input the new value: ")

    db.users.update_many(condition,{"$set" : {field_change:value_change}})

#function which updates 1 document
def update_one_document():
    condition = {}
    not_done = True
    while not_done:#same loop as in update_document
        field = input("Enter the field name you want to check: ")
        value = input("Enter the value for the key: ")
        condition.update({field:value})
        not_done = bool(int(input("Done?: Enter 0 for yes: ")))
        print(not_done)

    field_change = input("Enter the field you want to change: ")
    value_change = input("Input the new value: ")
    
    db.users.update_one(condition,{"$set" : {field_change:value_change}})

#function which reads all the documents and only returns username
def read_all_documents():
    curs = db.users.find({})
    for doc in curs:
        print(doc,"\n")

# this function reads and finds one document and only returns username
def read_one_document():
    curs = db.users.find_one({})
    print(curs)

#function which deletes 1 document from the collection given specified filter from user
def delete_one_document(doc):
    db.users.delete_one(doc)

#function which deletes all document from the collection given specified filter from user
def delete_many_documents(doc):
    db.users.delete_many(doc)

###mihle


##Ndemo
##Advanced query
def condition_find():
    curs = db.posts.find({"$and" : [{"username" : "diana33"},{"tags" : {"$in": ["feel"]}}]}, {"_id" :0 ,"content": 1})
    for doc in curs:
        print(doc,"\n")
#ndemo 
#array functions
def rem_arr():
    db.posts.update_many(
        {"username":"diana33"},
        {"$pull" : {"comment" : {"$in" : [0]}}}
    )

def output_cursor(cursor):
  for doc in cursor:
    print(doc)
## aggregation pipelines
def check_likes():
    curs = db.posts.aggregate(
        [
            {"$match" : {"username" : "diana33"}},
            {"$project" : {"_id" : 0, "username" : "diana33", "num_likes" : {"$size" : "$likes"}, "num_comments" : {"$size" : "$comments"}}},
        ]
    )
    output_cursor(curs)


#mihle
#advanced query
#finds all of michael48s posts or all posts with tech/new tags from any user
def find_michael_or_tags():
    curs = db.posts.find({
            "$or": [ {"username": "michael48"},]},{"_id": 0, "username": 1, "title": 1, "tags": 1})
    
    for doc in curs:
        print(doc, "\n")

#array functions
#removes an element in array 28 in friends field, users collection
def rem_arr():
    db.users.update_many({"username":"mquinn"},
                          {"$pull" : {"friends": {"$in" : [28]}}})

def output_cursor(cursor):
  for doc in cursor:
    print(doc)

rem_arr()

##function that add to an array in users collection, in friends field
def add_arr():
    db.users.update_one({"username": "davidfrench"}, {"$push" : {"friends": "ObjectId('68d6f41c00af4cdlae753b9')"}})


def output_cursor(cursor):
  for doc in cursor:
    print(doc)

add_arr()

def remove_arr():
    db.users.update_one({"username": "davidfrench"}, {"$pull": {"friends":24}})


def output_cursor(cursor):
  for doc in cursor:
    print(doc)

remove_arr()

#aggregation pipelines
def group_by_username():
    curs = db.users.aggregate([{"$match": {"username": "mquinn"}},{"$group": {
                "_id": "$username",  
                "total_friends": {"$sum": {"$size": "$friends"}},
                "total_activities": {"$sum": {"$size": "$recent_activity"}},
                "user_count": {"$sum": 1}}}])
    output_cursor(curs)
# -------------------------
# Menu System
# -------------------------

def menu():
    while True:

        check_likes()
        rem_arr()

        print("\n--- MongoDB Project Megnu ---")
        print("1. Create Document")
        print("2. Read All Documents")
        print("3. Update Document")
        print("4. Delete Document")
        print("5. Quit")

        choice = input("Enter choice: ") 
        
        if choice == "1":
            
            numChoice = (int(input("enter number of documents: ")))
            if numChoice >= 2:

                lst = []
                for i in range(numChoice):
                    name = input("Enter username: ")
                    email = input("Enter email: ")
                    lst.append({"username":name, "email":email})
                
                create_many(lst)

                
            else:
                name = input("Enter username: ")
                email = input("Enter email: ")
                create_document({"username": name, "email": email})

        elif choice == "2":
            user_in = input("enter 0 if you want to read 1 or enter anything if you want to read more: ")
            if user_in =="0":
                read_one_document()

            else: 
                read_all_documents()

    #calls function defined on line 61
        elif choice == "3":
            user_in = input("Do you want to insert 1 or many document, Type m for many and o for 1: ")
            if user_in == "m":
                update_document()
            else:
                update_one_document()
            

        
        elif choice == "4":
            user_in = input("Enter 0 if you want to delete one or enter anything else if you want to delete more: ")
            if user_in == "0":
                name = input("Enter username: ")
                email = input("Enter email: ")

                delete_one_document({"username": name, "email": email})
            else:
                name = input("Enter username: ")
                email = input("Enter email: ")

                delete_many_documents({"username": name, "email": email})
        elif choice == "5":
            print("Exiting...")
            quit()


        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()

