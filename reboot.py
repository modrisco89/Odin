
import subprocess #used to run commands from python
import time
from datetime import datetime, timedelta
import pymongo
import string
from dotenv import load_dotenv
import os
load_dotenv()

ec2 = os.environ.get("sIp")
ec2db = os.environ.get("dbIp")

myclient = pymongo.MongoClient("mongodb://" + ec2db +":27017/")
mydb = myclient["ODIN"]
myColAction = mydb["admins"]



reboot_cmd = [
    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-i", "Mike.pem",
    "ec2-user@" + ec2,
    "sudo reboot"
]

mydict = {"date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "action": "Reboot", "firstName": "Michael Martin", "lastName": "O'Driscoll", "email": "geralt.odriscoll@gmail.com"}
myColAction.insert_one(mydict)

subprocess.run(reboot_cmd, capture_output=True, text=True)
