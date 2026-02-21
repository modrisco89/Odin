
import subprocess #used to run commands from python
from dotenv import load_dotenv
import os
load_dotenv()

ec2 = os.environ.get("sIp")

reboot_cmd = [
    "ssh",
    "-i", "Mike.pem",
    "ec2-user@" + ec2,
    "sudo reboot"
]


subprocess.run(reboot_cmd, capture_output=True, text=True)
