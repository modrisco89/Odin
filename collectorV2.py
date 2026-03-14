import pymongo
import os
import boto3
import subprocess #used to run commands from python
import time #used for the delay to wait for the web server to be up and running
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ec2db = os.environ.get("dbIp")
bastion = os.environ.get("bastion")
ec2client = boto3.client("ec2", region_name="us-east-1")
elbv2 = boto3.client("elbv2", region_name="us-east-1")

tg = "arn:aws:elasticloadbalancing:us-east-1:159726579547:targetgroup/VenuelyTG2/889c6eee0403dded"
targets = elbv2.describe_target_health(TargetGroupArn=tg)

myclient = pymongo.MongoClient("mongodb://" + ec2db + ":27017/")
mydb = myclient["ODIN"]
mycol =mydb["instanceStats"]
while(True):
	for _ in range(3):
    		targets = elbv2.describe_target_health(TargetGroupArn=tg)
    		healthy_ids = [t["Target"]["Id"] for t in targets["TargetHealthDescriptions"]
                	if t["TargetHealth"]["State"] == "healthy"]
    		if healthy_ids:
			instance_id = healthy_ids[0]
			break
		time.sleep(20)
	else:
    		print("No healthy instances after 3 tries. Skipping this iteration.")
    		time.sleep(30)
    		continue
	instance_name = "MonitoredDatabase"
	instance_id = healthy_ids[0]

	response2 = ec2client.describe_instances(
	    Filters=[
		{
		    "Name": "tag:Name",
		    "Values": [instance_name]
		},
		{
		    "Name": "instance-state-name",
		    "Values": ["running"]
		}
	    ]
	)

	for reservation in response2["Reservations"]:
		for instance in reservation["Instances"]:
			dbprivate_ip = instance["PrivateIpAddress"]
			instance_id2 = instance["InstanceId"]


	response = ec2client.describe_instances(InstanceIds=[instance_id])
	instance = response['Reservations'][0]['Instances'][0]
	host = instance.get('PrivateIpAddress')
	print("Host for SSH:", host)
	
	cpu_cmd = [
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + bastion,
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + host,
	    "top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'"
	]

	cmd = (
	    "RX1=$(cat /sys/class/net/enX0/statistics/rx_bytes); "
	    "sleep 1; "
	    "RX2=$(cat /sys/class/net/enX0/statistics/rx_bytes); "
	    "awk 'BEGIN {printf \"%.3f\\n\", (RX2-RX1)*8/1000000}'"
	)

	bw_cmd = [
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + bastion,
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + host,
	    cmd
	]


	uptime_cmd = [        "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + bastion,
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + host,
	   "uptime -p"
	]

	mem_cmd= [        "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + bastion,
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + host,
	   "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2}'"
	]

	stor_cmd= [        "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + bastion,
	    "ssh",
	    "-o", "StrictHostKeyChecking=no",
	    "-i", "Mike.pem",
	    "ec2-user@" + dbprivate_ip,
		"df -h / | awk 'NR==2 {print $5}'"
	]

	
	cpu = subprocess.run(cpu_cmd, capture_output=True, text=True)
	uptime = subprocess.run(uptime_cmd, capture_output=True, text=True)
	memUsed = subprocess.run(mem_cmd, capture_output=True, text=True)
	storUsed = subprocess.run(stor_cmd, capture_output=True, text=True)
	bandwidth = subprocess.run(bw_cmd, capture_output=True, text=True)
	mydict = {
		"time": datetime.now(),
		"CPU": cpu.stdout.strip(),
		"uptime": uptime.stdout.strip(),
		"memUsed": memUsed.stdout.strip(),
		"storUsed": storUsed.stdout.strip(),
		"bandwidth": bandwidth.stdout.strip()
	}
	x = mycol.insert_one(mydict)
	time.sleep(30)






