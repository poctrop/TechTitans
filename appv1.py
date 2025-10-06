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

'''nkateko'''

def find_posts_with_all_tags():
    """
    Find posts that contain all the tags the user enters.
    """
    print("\n--- Find Posts with All Tags ---")

    tags_input = input("Enter tags to search for (comma-separated): ")
    tags_list = []

    # Split the input and remove spaces from each tag
    tags = tags_input.split(",")
    for tag in tags:
        clean_tag = tag.replace(" ", "")
        tags_list.append(clean_tag)

    # Search for posts that contain all the tags
    query = {"tags": {"$all": tags_list}}
    fields = {"_id": 0, "username": 1, "title": 1, "content": 1, "tags": 1}
    cursor = db.posts.find(query, fields)

    print("\nPosts containing all these tags:", tags_list)
    output_cursor(cursor)


def find_users_with_exact_friends():
    """
    Find users with exact number of friends using $size
    """
    print("\n--- Find Users with Exact Friend Count ---")
    friend_count = int(input("Enter exact number of friends: "))
    
    cursor = db.users.find({
        "friends": {"$size": friend_count}
    }, {"_id": 0, "username": 1, "email": 1, "friends": 1})
    
    print(f"Users with exactly {friend_count} friends:")
    output_cursor(cursor)

def find_active_users_by_activity_size():
    """
    Find users based on recent activity array size
    """
    print("\n--- Find Active Users ---")
    min_activities = int(input("Enter minimum recent activities: "))
    
    pipeline = [
        {
            "$addFields": {
                "activity_count": {"$size": "$recent_activity"}
            }
        },
        {
            "$match": {
                "activity_count": {"$gte": min_activities}
            }
        },
        {
            "$project": {
                "_id": 0,
                "username": 1,
                "activity_count": 1,
                "recent_activity": 1
            }
        },
        {
            "$sort": {"activity_count": -1}
        }
    ]
    
    cursor = db.users.aggregate(pipeline)
    print(f"Users with at least {min_activities} recent activities:")
    output_cursor(cursor)

def top_most_liked_posts():
    """
    Find the top 10 most liked posts
    """
    print("\n--- Top 10 Most Liked Posts ---")
    
    pipeline = [
        {
            "$match": {
                "likes": {"$exists": True}
            }
        },
        {
            "$project": {
                "title": 1,
                "username": 1,
                "content": 1,
                "like_count": {"$size": "$likes"},
                "comment_count": {"$size": "$comments"},
                "engagement_rate": {
                    "$divide": [
                        {"$size": "$likes"},
                        {"$max": [1, {"$size": "$comments"}]}
                    ]
                }
            }
        },
        {
            "$sort": {"like_count": -1}
        },
        {
            "$limit": 10
        }
    ]
    
    cursor = db.posts.aggregate(pipeline)
    print("Top 10 most liked posts:")
    output_cursor(cursor)

def most_active_users():
    """
    Find users with highest engagement (posts + comments + likes)
    """
    print("\n--- Most Active Users ---")
    
    pipeline = [
        {
            "$lookup": {
                "from": "posts",
                "localField": "username",
                "foreignField": "username",
                "as": "user_posts"
            }
        },
        {
            "$addFields": {
                "post_count": {"$size": "$user_posts"},
                "total_likes_given": {"$size": "$liked_posts"},
                "total_comments": {"$size": "$comments"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "username": 1,
                "post_count": 1,
                "total_likes_given": 1,
                "total_comments": 1,
                "engagement_score": {
                    "$add": [
                        "$post_count",
                        "$total_likes_given",
                        "$total_comments"
                    ]
                }
            }
        },
        {
            "$sort": {"engagement_score": -1}
        },
        {
            "$limit": 10
        }
    ]
    
    cursor = db.users.aggregate(pipeline)
    print("Top 10 most active users:")
    output_cursor(cursor)

def popular_tags_analysis():
    """
    Analyze most popular tags and their engagement
    """
    print("\n--- Popular Tags Analysis ---")
    
    pipeline = [
        {
            "$unwind": "$tags"
        },
        {
            "$group": {
                "_id": "$tags",
                "total_posts": {"$sum": 1},
                "avg_likes": {"$avg": {"$size": "$likes"}},
                "avg_comments": {"$avg": {"$size": "$comments"}},
                "total_engagement": {
                    "$sum": {
                        "$add": [
                            {"$size": "$likes"},
                            {"$size": "$comments"}
                        ]
                    }
                }
            }
        },
        {
            "$sort": {"total_engagement": -1}
        },
        {
            "$limit": 15
        }
    ]
    
    cursor = db.posts.aggregate(pipeline)
    print("Most popular tags by engagement:")
    output_cursor(cursor)

def user_friend_network_analysis():
    """
    Analyze user friend networks and social circles
    """
    print("\n--- User Friend Network Analysis ---")
    
    pipeline = [
        {
            "$match": {
                "friends": {"$exists": True}
            }
        },
        {
            "$addFields": {
                "friend_count": {"$size": "$friends"},
                "network_size": {"$add": [{"$size": "$friends"}, 1]}  # +1 for the user themselves
            }
        },
        {
            "$project": {
                "_id": 0,
                "username": 1,
                "friend_count": 1,
                "network_size": 1,
                "social_category": {
                    "$switch": {
                        "branches": [
                            {"case": {"$lt": ["$friend_count", 10]}, "then": "Small"},
                            {"case": {"$lt": ["$friend_count", 50]}, "then": "Medium"},
                            {"case": {"$lt": ["$friend_count", 100]}, "then": "Large"}
                        ],
                        "default": "Very Large"
                    }
                }
            }
        },
        {
            "$sort": {"friend_count": -1}
        }
    ]
    
    cursor = db.users.aggregate(pipeline)
    print("User friend network analysis:")
    output_cursor(cursor)


def posts_with_high_engagement():
    """
    Find posts with high engagement (both likes and comments)
    """
    print("\n--- High Engagement Posts ---")
    
    min_likes = int(input("Enter minimum likes: ") or "10")
    min_comments = int(input("Enter minimum comments: ") or "5")
    
    pipeline = [
        {
            "$match": {
                "likes": {"$exists": True},
                "comments": {"$exists": True}
            }
        },
        {
            "$addFields": {
                "like_count": {"$size": "$likes"},
                "comment_count": {"$size": "$comments"}
            }
        },
        {
            "$match": {
                "like_count": {"$gte": min_likes},
                "comment_count": {"$gte": min_comments}
            }
        },
        {
            "$project": {
                "_id": 0,
                "username": 1,
                "title": 1,
                "like_count": 1,
                "comment_count": 1,
                "engagement_ratio": {
                    "$divide": ["$like_count", "$comment_count"]
                }
            }
        },
        {
            "$sort": {"like_count": -1}
        }
    ]
    
    cursor = db.posts.aggregate(pipeline)
    print(f"Posts with at least {min_likes} likes and {min_comments} comments:")
    output_cursor(cursor)






# -------------------------
# Menu System
# -------------------------

def social_media_analytics_menu():
    """New menu for social media analytics"""
    while True:
        
        print("\n      SOCIAL MEDIA ANALYTICS DASHBOARD")
       
        
        print("\n\n ARRAY OPERATIONS:")
        print("1.  Find posts with ALL specific tags")
        print("2.  Find users with exact friend count")
        print("3.  Find active users by activity level")
        
        print("\n AGGREGATION ANALYTICS:")
        print("4.  Top 10 most liked posts")
        print("5.  Most active users")
        print("6.  Popular tags analysis")
        print("7.  User friend network analysis")
        print("8.  High engagement posts")
        print("9.  Back to main menu")
        
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == "1":
            find_posts_with_all_tags()
        elif choice == "2":
            find_users_with_exact_friends()
        elif choice == "3":
            find_active_users_by_activity_size()
        elif choice == "4":
            top_most_liked_posts()
        elif choice == "5":
            most_active_users()
        elif choice == "6":
            popular_tags_analysis()
        elif choice == "7":
            user_friend_network_analysis()
        elif choice == "8":
            posts_with_high_engagement()
        elif choice == "9":
            break
        else:
            print("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

def advanced_queries_menu():
    """Menu for the existing MongoDB advanced queries"""
    while True:
        print("\n Advanced MongoDB Queries ")
        print("1. Query with $and and $in operators")
        print("2. Aggregation pipeline with $size")
        print("3. Group aggregation with array sizes") 
        print("4. Back to main menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            condition_find()
        elif choice == "2":
            check_likes()
        elif choice == "3":
            group_by_username()
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")
        
        input("\nPress Enter to continue...")

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

