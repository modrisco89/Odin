from typing import List
import json
import os
import time
import random
import string
import pymongo
import subprocess
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from bson import json_util

from dotenv import load_dotenv
reboot = False;
load_dotenv()

ec2db = os.environ.get("dbIp")
ec2 = os.environ.get("sIp")

myclient = pymongo.MongoClient("mongodb://" + ec2db +":27017/")
mydb = myclient["ODIN"]
mycol = mydb["instanceStats"]
myColOpinion = mydb["opinions"]
myColAction = mydb["admins"]

reboot_cmd = [
    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-i", "Mike.pem",
    "ec2-user@" + ec2,
    "sudo reboot"
]

# -------- Tools --------
@tool
def give_data():
	"""Read and return the contents of a JSON."""
	return json_util.dumps(list(mycol.find().sort("time",-1).limit(10)), indent=2)

@tool	
def determine_reboot():
	"""set reboot to True"""
#	mydict = {"date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "action": "Reboot", "firstName": "Odin", "lastName": "Borson"}
#	myColAction.insert_one(mydict)
# subprocess.run(reboot_cmd, capture_output=True, text=True)
	global reboot
	reboot = True
	return reboot
	
def reboot_not_needed():
	"""set reboot to false"""
	global reboot
	reboot = False
	return reboot
		
TOOLS = [give_data, determine_reboot, reboot_not_needed]

llm = ChatOpenAI(model="gpt-4", temperature=0)

SYSTEM_MESSAGE = (
    "You are Odin, a helpful assistant that monitors system health. "
    "You will also try to read data from give_data, this will give you a dataset about CPU, used memory percentage and uptime of a server, and tell me about the data if the data is healthy or not"
    "You will also determine_reboot by setting reboot to true if there are 10 consecutive datapoints in the latest 10 data points from give_data of CPU containing 100 percent spikes, otherwise check if reboot_not_needed"
    "You will also give important statistics on the dataset" 
    "storUsed is database storage, it's a seperate server"
)

agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_MESSAGE)


def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    """Single-turn agent runner with automatic tool execution via LangGraph."""
    try:
        result = agent.invoke(
            {"messages": history + [HumanMessage(content=user_input)]},
            config={"recursion_limit": 50}
        )
        # Return the last AI message
        return result["messages"][-1]
    except Exception as e:
        # Return error as an AI message so the conversation can continue
        return AIMessage(content=f"Error: {str(e)}\n\nPlease try rephrasing your request or provide more specific details.")


if __name__ == "__main__":
    print("=" * 60)
    print("Odin is watching :D")
    print("=" * 60)

    history: List[BaseMessage] = []

    while True:
        user_input = "From the dataset, tell me if I should be worried or not (note storUsed is on a seperate server known as a ""Database"", and determine a reboot only if the latest 10 data points have consecutive CPU 100% spikes in a row otherwise determine if a reboot is not needed, if uptime is uptime is between 0 to 10 minutes a reboot is not needed, Also say it like your a god, since you're name is Odin".strip()
        print("Odin is analzing data")
        print("Odin: ", end="", flush=True)
        response = run_agent(user_input, history)
        print(response.content)
        print()         
        mydict = {"date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "opinion": str(response.content), "rebootRequired": reboot}
        myColOpinion.insert_one(mydict)
        # Update conversation history
        history += [HumanMessage(content=user_input), response]
        time.sleep(300)
