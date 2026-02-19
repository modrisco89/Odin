
import subprocess #used to run commands from python
ec2 = "50.19.4.28"

reboot_cmd = [
    "ssh",
    "-i", "Mike.pem",
    "ec2-user@" + ec2,
    "sudo reboot"
]


subprocess.run(reboot_cmd, capture_output=True, text=True)
