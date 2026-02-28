import pymongo
import os
import subprocess #used to run commands from python
import time #used for the delay to wait for the web server to be up and running
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ec2db = os.environ.get("dbIp")
ec2 = os.environ.get("sIp")

cpu_cmd = [
    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-i", "Mike.pem",
    "ec2-user@" + ec2,
    "top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'"
]

uptime_cmd = [    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-i", "Mike.pem",
   "ec2-user@"+ ec2,
   "uptime -p"
]

mem_cmd= [    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-i", "Mike.pem",
   "ec2-user@" + ec2,
   "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2}'"
]

stor_cmd= [    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-i", "Mike.pem",
   "ec2-user@" + ec2db ,
   "df -h / | awk 'NR==2 {print $5}'"
]


myclient = pymongo.MongoClient("mongodb://" + ec2db + ":27017/")
#print(myclient.list_database_names())
mydb = myclient["ODIN"]
mycol =mydb["instanceStats"]

while(True):
	cpu = subprocess.run(cpu_cmd, capture_output=True, text=True)
	uptime = subprocess.run(uptime_cmd, capture_output=True, text=True)
	memUsed = subprocess.run(mem_cmd, capture_output=True, text=True)
	storUsed = subprocess.run(stor_cmd, capture_output=True, text=True)
	mydict = {"time": datetime.now(), "CPU": cpu.stdout.strip(), "uptime": uptime.stdout.strip(), "memUsed": memUsed.stdout.strip(), "storUsed": storUsed.stdout.strip()}
	x = mycol.insert_one(mydict)
	time.sleep(30)

