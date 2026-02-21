import os
import subprocess #used to run commands from python
from dotenv import load_dotenv
load_dotenv()

ec2db = os.environ.get("dbIp")
ec2 = os.environ.get("sIp")


db_startcmd = [
    "ssh",
    "-i", "Mike.pem",
    "ec2-user@" + ec2db,
    "sudo systemctl stop mongod && sudo systemctl start mongod && sudo mongod -dbpath db --bind_ip_all"
]

subprocess.run(db_startcmd, capture_output=True, text=True)


