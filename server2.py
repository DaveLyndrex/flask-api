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


#########################################################################################################################

# R E A D
@app.route("/signature", methods=["GET"])
def get_signature():
    try:
        data = list(db.signature.find())
        #converting id into a string
        for signatures in data:
            signatures["_id"] = str(signatures["_id"])
        return Response(response= json.dumps(data),
        status=200,
        mimetype="application/json" #to pass a json data
        )
    
    except Exception as ex:
        print("*****************************")
        print(ex)
        print("*****************************")
        return Response(response= json.dumps({"Message": "Cannot Read Signature"}), #i will tell the client that I will pass a data
        status=500,
        mimetype="application/json" #to pass a json data
        )
#############################################################################################################



@app.route("/signature", methods = ['POST'])
def created_user_signature():
    try:
        signature = {"firstname" : request.json["firstname"], "lastname" : request.json["lastname"], 
                    "position" : request.json["position"], "mobileNumber" : request.json["mobileNumber"], "image" : request.json["image"]}
        #signature = {"firstname" : request.form["firstname"], "lastname" : request.form["lastname"], 
                    #"position" : request.form["position"], "mobileNumber" : request.form["mobileNumber"], "image" : request.json["image"]}
        #signature = {"firstname" : "Dave Lyndrex", "lastname" : "Millan", "position" : "Backend Developer",
                    #"mobileNumber" : "09223434323", "email" : "dave@gmail.com", "image" : ""}
        #intern = {"firstname" : request.form["firstname"], "lastname" : request.form["lastname"]}
        #intern = {"firstname" : "Dave Lyndrex", "lastname" : "Millan"}
        dbResponse = db.signature.insert_one(signature)#get a response, from the db(cloud_ninja). interns(collection)-it will create automatically... and insert the intern which is a json object
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

@app.route("/signature/<signature_id>", methods=["PUT"])
def update_user(signature_id):
    #return id
    try:
        dbResponse = db.signature.update_one(
            #in here, we can now use the bson object id that we impported
            {"_id" : ObjectId(signature_id)},
            {"$set" : {"firstname" : request.json["firstname"], "lastname" : request.json["lastname"], "position" : request.json["position"],
            "mobileNumber" : request.json["mobileNumber"], "email" : request.json["email"], "image" : request.json["image"]}}
        )
       # for attr in dir(dbResponse):
        #    print(f"************{attr}**************")

        if dbResponse.modified_count == 1:   
            return Response(
                response = json.dumps(
                {"Message" : " Signature Updated"}),
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
            response= json.dumps({"Message": "Cannot Update Signature",
             }),
            status=500,#500 is an internal mserver error
            mimetype="application/json" #to pass a json data
        )

#########################################################################################################################

# D E L E T E
@app.route("/signature/<signature_id>", methods = ["DELETE"])
def delete_user_signature(signature_id):
    try:
        dbResponse = db.signature.delete_one({"_id" : ObjectId(signature_id)})  #bson activate

       # for attr in dir(dbResponse):
        #    print(f"*****{attr}******")
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"Message": "Signature Deleted", "signature_id":f"{signature_id}"}),
                status=200,
                mimetype="application/json" #to pass a json data
            )
        else:
            return Response(
                response = json.dumps(
                    {"message" : "Signature not found", "signature_id":f"{signature_id}"}),
                    status = 200,
                    mimetype = "application/json"
            )

    except Exception as ex:
        print("*******************************")
        print(ex)
        print("*******************************")
        return Response(
            response= json.dumps({"Message": "Cannot Delete Signature. Signature not found",
             }),
            status=500,#500 is an internal message error
            mimetype="application/json" #to pass a json data
        )

if __name__ == "__main__":
    app.run(port=80, debug=True)