from flask import Flask, Response, request
import json
import pymongo
from bson.objectid import ObjectId  #bson is a library that makes the object id a text

app = Flask(__name__)

###########################################################################################################
try:
    #connect to mongo
    mongo = pymongo.MongoClient(host="localhost", 
    port=27017, 
    serverSelectionTimeoutMS = 1000) #serverSelec.... will allow us to catch exception
    
    #creating database variable, connecting to mongo client and the database we want to use
    db = mongo.cloud_ninja
    mongo.server_info()#trigger exception if cannot connect to database
except:
    print("ERROR = Cannot connect to db")



#############################################################################################################
# R E A D
@app.route("/users", methods=["GET"])
def get_user():
    try:
        data = list(db.interns.find())
        #converting id into a string
        for interns in data:
            interns["_id"] = str(interns["_id"])
        return Response(response= json.dumps(data),
        status=200,
        mimetype="application/json" #to pass a json data
        )
    
    except Exception as ex:
        print("*****************************")
        print(ex)
        print("*****************************")
        return Response(response= json.dumps({"Message": "Cannot Read User"}), #i will tell the client that I will pass a data
        status=500,
        mimetype="application/json" #to pass a json data
        )



#####################################################################################################################
# C R E A T E
@app.route("/users", methods = ['POST'])
def created_user():
    try:
        intern = {"firstname" : request.json["firstname"], "lastname" : request.json["lastname"]}
        #intern = {"firstname" : request.form["firstname"], "lastname" : request.form["lastname"]}
        #intern = {"firstname" : "Dave Lyndrex", "lastname" : "Millan"}
        dbResponse = db.interns.insert_one(intern)#get a response, from the db(cloud_ninja). interns(collection)-it will create automatically... and insert the intern which is a json object
        print(dbResponse.inserted_id) 
     #   for attr in dir(dbResponse):#key that we use from the db response
      #      print(attr) 
        return Response(
            response= json.dumps({"Message": "user created",
             "id":f"{dbResponse.inserted_id}"
             }), #i will tell the client that I will pass a data
            status=200,
            mimetype="application/json" #to pass a json data
        )
    except Exception as ex:
        print("*****************************")
        print(ex)
        print("*****************************")


########################################################################################################################
# U P D A T E

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    #return id
    try:
        dbResponse = db.interns.update_one(
            #in here, we can now use the bson object id that we impported
            {"_id" : ObjectId(id)},
            {"$set" : {"firstname" : request.form["firstname"]}}
        )
       # for attr in dir(dbResponse):
        #    print(f"************{attr}**************")

        if dbResponse.modified_count == 1:   
            return Response(
                response = json.dumps(
                {"Message" : " User Updated"}),
                status=200,
                mimetype="application/json" 
        )
        else:
            return Response(
                response = json.dumps(
                    {"message" : "Nothing to Update"}),
                    status = 200,
                    mimetype = "application/json"
            )

    except Exception as ex:
        print("**************")
        print(ex)
        print("**************")
        return Response(
            response= json.dumps({"Message": "Cannot Update User",
             }),
            status=500,#500 is an internal mserver error
            mimetype="application/json" #to pass a json data
        )


##################################################################################################################################
# D E L E T E
@app.route("/users/<id>", methods = ["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.interns.delete_one({"_id" : ObjectId(id)})  #bson activate

       # for attr in dir(dbResponse):
        #    print(f"*****{attr}******")
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"Message": "User Deleted", "id":f"{id}"}),
                status=200,
                mimetype="application/json" #to pass a json data
            )
        else:
            return Response(
                response = json.dumps(
                    {"message" : "User not found", "id":f"{id}"}),
                    status = 200,
                    mimetype = "application/json"
            )

    except Exception as ex:
        print("*******************************")
        print(ex)
        print("*******************************")
        return Response(
            response= json.dumps({"Message": "Cannot Delete User",
             }),
            status=500,#500 is an internal message error
            mimetype="application/json" #to pass a json data
        )


    
if __name__ == "__main__":
    app.run(port=80, debug=True)