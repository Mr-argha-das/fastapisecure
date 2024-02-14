from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from usermodel import User
from profilemodel import UserProfile
from mongoengine import connect, Document, StringField
from fastapi.responses import JSONResponse
from addproject import ProjectsModel
from userdata import UserContacts
from userwithdrawal import UserWithdrawal
from usermpin import UserMPIN
from citysmodel import CityModel
import json
app = FastAPI()
import csv

connect('fastapi', host='mongodb+srv://sahiljoya11:sahil1122@cluster0.syubkoh.mongodb.net/fastapi')



@app.get("/user-list")
async def getUser():
    users = User.objects.all()
    print(users)
    user_json = users.to_json()
    json_data = json.loads(user_json)
    return {"message": "User data successfully", "data":json_data, "status":True}
    return users.to_json()

@app.post("/users-create")
async def create_user(name: str, email: str, password: str, phone: str,):
    findUser = User.objects(email=email)
    findUserPhone = User.objects(phone=phone)
    if findUser or findUserPhone:
        return {"message": "This mail or phone already used", "data": None, "status":False}
    
    user = User(name=name, email=email, password=password, phone=phone, countryCode="91")
    user.save()
    user_json = user.to_json()
    json_data = json.loads(user_json)
    
    return {"message": "User created successfully", "data":json_data, "status":True}

@app.post("/create-user-mpin")
async def createusermpin(userid: str, mpin: str):
    data = UserMPIN(userid=userid,mpin=mpin)
    data.save()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "MPIN added",
        "data":fromjson,
        "status":True
    }
    
@app.post("/user-forget-phone")
async def forgetPassword(phone: str, password: str):
    user = User.objects(phone=phone).first()
    if user:
        user.password = password
        user.save()
        return {
            "message": "Password update",
            "status": True
        }
    return {
        "message": "user not  found",
        "status": False
    }
    
@app.post("/user-forget-email")
async def forgetPassword(email: str, password: str):
    user = User.objects(email=email).first()
    if user:
        user.password = password
        user.save()
        return {
            "message": "Password update",
            "status": True
        }
    return {
        "message": "user not  found",
        "status": False
    }

@app.post("/user-login")
async def loginMailPassword(email: str, password: str):
    userfind = User.objects(email=email).first()
    print("////////////////////////////////////////////")
    print(userfind)
    user = userfind.to_json()
    
    if userfind:
        data = UserMPIN.objects(userid=str(userfind.id))
        tojson = data.to_json()
        fromjson = json.loads(tojson)
        if userfind.password == password:
            json_data = json.loads(user)
            return {
                "message":"Login Success",
                "data": json_data,
                "mpin": fromjson,
                "status": True
            }
        else:
            return {
                "message":"Login Faild",
                "data": None,
                "mpin": None,
                "status": False
            }
    return  {
                "message":"User not found",
                "data": None,
                "mpin": None,
                "status": False
            }

@app.post("/user-login-phone")
async def userloginbyphone(phone: str):
    userfind = User.objects(phone=phone).first()
    if userfind:
        user = userfind.to_json()
        json_data = json.loads(user)
        return {
            "message": "User found",
            "data": json_data,
            "status": True
        }
    return {
        "message": "User not found",
        "data": None,
        "status": False
    }           
        
@app.post("/add-user-profile")
async def addUserProfile(userId: str, upiId: str, profileImage: str, gender: str, age: str, location: str):
    profileData = UserProfile(user_id=userId, upiId=upiId, profileImage=profileImage,gender=gender, age=age, location=location)
    profileData.save()
    return {
            "message": "UserProfile Added",
            "status": True
        }
@app.get("/get-user-profile/{userid}")
async def findProfile(userid: str):
    profileData= UserProfile.objects(user_id=userid).first()
    if profileData:
        profile = profileData.to_json()
        json_data = json.loads(profile)
        return {
            "message":"Profile Data found",
            "data": json_data,
            "status":True
        }
    else:
        return {
            "message": "Profile Not adde yet",
            "data":None,
            "status":False
        }

@app.put("/update-profile/{userid}")
async def updateprofile(userid: str, upid:str, profileImage:str, location: str):
    profile = UserProfile.objects(user_id= userid).first()
    profile.upiId = upid
    profile.profileImage = profileImage
    profile.location = location
    profile.save()
    return {
        "message": "Profile updated success",
        "status": True
    }
    
@app.post("/add-project")
async def addProject(projectTitle:str, url: str, location: str):
    project = ProjectsModel(projectTitle=projectTitle, url=url, location=location)
    project.save()
    return {
        "message":"Project add",
        "status":True,
    }

@app.get("/all-projects")
async def getAllProjects():
    projects = ProjectsModel.objects.all()
    jsondata = projects.to_json()
    json_data = json.loads(jsondata)
    return {
        "message":"Here is all projects",
        "data":json_data,
        "status":True
    }
    
@app.get("/get-all-profiles")
async def getallProfile():
    profiledata = UserProfile.objects.all()
    data = profiledata.to_json()
    jsondata= json.loads(data)
    return jsondata

@app.post("/update-user-data")
async def updateUserData(userid:str, userdata: str):
    userdata = UserContacts(userid=userid, userData=userdata)
    userdata.save()
    return {
        "status":True
    }
    
@app.get("/get-user-xxxx-data")
async def getUserData():
    userData = UserContacts.objects.all()
    data = userData.to_json()
    jsonData = json.loads(data)
    return jsonData

@app.post("/user-withdrawal-req")
async def addUSerWithdrawal(userid: str, amount:str, name: str):
    userWithdrawal = UserWithdrawal(userid=userid, amount=amount, status=False, name=name)
    userWithdrawal.save()
    return {
        "message":"Your withdrawal requiest add",
        "status": True
    }


@app.put("/update-user-payment-byadmin")
async def updaqteUserPaymentByAdmin(primary_key:str, trnx: str, status: bool):
    data = UserWithdrawal(primary_key=primary_key).first()
    data.trnx = trnx
    data.status = status
    data.save()
    return {
        "message":"Withdrwal update",
        "status": True
    }
    
@app.get("user-withdrawal-req-list/{userID}")
async def userWithdrawalreqList(userID: str):
    data = UserWithdrawal.objects(userid=userID).first()
    if data:
        tojson = data.to_json()
        json_data = json.loads(tojson)
        return{
            "message":"Hers is your List",
            "data":json_data,
            "status":True
        }
    else:
        return {
        "messages":"Not List found",
        "data": None,
        "status":False
    }    
@app.get("/get-all-withdrawal-list")
async def getAllWithdrawalList():
    data = UserWithdrawal.objects.all()
    tojson = data.to_json()
    json_data = json.loads(tojson)
    return {
        "message":"Here is your withdrawal requiest",
        "data": json_data,
        "status":True
    }
    
@app.get("/get-all-cityes")
async def getallcityes():
    data = CityModel.objects.all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Here is citys",
        "data":fromjson,
        "status":True
    }
@app.get("/search-citys/{cityesname}")
async def searchCityes(cityesname: str):
    data = CityModel.objects(cityname__icontains=cityesname).all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"result",
        "data":fromjson,
        "status":True    
    }