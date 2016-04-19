# 1.] Requires an instance of MongoDB running on port 27017 (default port):
#	  cd C:\Program Files\MongoDB\Server\3.2\bin (or where you installed it)
#	  mongod.exe --dbpath C:\Users\Ian\Desktop\CoachWatson (or any empty directory)
#	  mongo.exe
# 2.] Requires pymongo to be installed/included. (pip install pymongo)

# Explanation: Some example queries and operations for our MongoDB database.  Uses
# PyMongo to input example data into the database.

from pymongo import MongoClient
from datetime import datetime

# Connect to the local Mongo client which is running.
client = MongoClient()
db = client.CoachWatson # "CoachWatson" is the name of the desired DATABASE.
users = db.Users # "Users" is the name of the desired COLLECTION.

# So, one instance of MongoDB can have multiple databases, and each database can have
# multiple collections.

# With MongoDB, a data element does not need to have a prior table set up to
# insert it.  Let's make up some example "user" data elements and
# insert them straight away into the collection.  MongoDB does the rest for us.
list_of_users = [
	{'user_id': 1, 'username': 'pedelose.1@osu.edu', 'password': 'Tiranno123', 'firstname': 'Tyler',
		'last_name': 'Pedelose', 'date': '2/15/2016'},
	{'user_id': 2, 'username': 'weber.595@osu.edu', 'password': 'Weber123', 'firstname': 'Ian',
		'last_name': 'Weber', 'date': '2/15/2016'},
	{'user_id': 3, 'username': 'watson@osu.edu', 'password': 'watson123', 'firstname': 'Thomas',
		'last_name': 'Watson', 'date': '2/15/2016'}
]
result = users.insert_many(list_of_users)

# Now let's add data to a different collection.  This collection is the User_Profiles
# collection which contains data such as gender, height, weight, age, etc.
user_profiles = db.User_Profiles
list_of_user_profiles = [
	{'user_id': 1, 'gender': 'Male', 'height': '175', 'weight': '170', 'age':'22'},
	{'user_id': 2, 'gender': 'Male', 'height': '165', 'weight': '170', 'age':'23'},
	{'user_id': 3, 'gender': 'Male', 'height': '155', 'weight': '150', 'age':'21'}
]
result = user_profiles.insert_many(list_of_user_profiles)

# Same thing again, this time adding to the QA_Histories collection which contains
# information about a user's previously asked questions.
qa_histories = db.QA_Histories
list_of_qa_histories = [
	{'user_id': 1, 'date': '2/16/2016', 'question': 'How do I perform a bicep curl?'},
	{'user_id': 2, 'date': '2/16/2016', 'question': 'How do I perform a jumping jack?'},
	{'user_id': 3, 'date': '2/16/2016', 'question': 'I want to know more about recommended daily nutrition for females of age 18-30.'}
]
result = qa_histories.insert_many(list_of_qa_histories)

# Same thing again, this time we add data to the Exercises collection.
exercises = db.Exercises
list_of_exercises = [
	{'exercise_name': 'Bicep Curl', 'exercise_img': 'bicep_curl.jpg', 'type': 'Arms'},
	{'exercise_name': 'Running', 'exercise_img': 'running.jpg', 'type': 'Cardio'},
	{'exercise_name': 'Squat', 'exercise_img': 'reg_squat.jpg', 'type': 'Legs'}
]
result = exercises.insert_many(list_of_exercises)

# ----- End of inputting example data into the CoachWatson database. -----

# Now let's do some example queries and operations on the data we put in...

# Let's say I want to know how many users we have currently in our database.
How_Many_Users = users.count()
print("We currently have " + str(How_Many_Users) + " users in our database. \n")

# Let's say that a user inputs his username and password on the login boxes on
# our main page.  We want to check those against the database.
cursor = users.find({'username' : 'pedelose.1@osu.edu'})
print("\n Any matches for username tiranno?: \n")
for document in cursor:
    print(document)

# Same thing but let's say he typed his username wrong.  Nothing should be printed.
cursor = users.find({'username': 'yiranno'})
print("\n Any matches for username yiranno?: \n")
for document in cursor:
    print(document)

# Let's say he entered in his username correctly but mistyped his password.
cursor = users.find({'username' : 'weber.595', 'password': 'Wever123'})
print("\n Any matches for username weber.595 with password Wever123?: \n")
for document in cursor:
    print(document)

# Let's say he corrected his password.
cursor = users.find({'username' : 'weber.595', 'password': 'Weber123'})
print("\n Any matches for username weber.595 with password Weber123?: \n")
for document in cursor:
    print(document)
