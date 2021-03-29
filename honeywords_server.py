import json
import random
from flask import *
from utils import *
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--run_mode", type=str, default="tail")
parser.add_argument("--db_name", type=str, default="db_tail_honeywords.json")
args = parser.parse_args()
app = Flask("honeywords_server")

try:
    print("Loading HoneyWords DB")
    honeywords_db = load_db_from_file(args.db_name)
except Exception as e:
    print("Error:", e, "creating new HoneyWords DB...")
    honeywords_db = {}
    dump_db_to_file(honeywords_db, args.db_name)
    print("New HoneyWords DB is at args.db_name")

"""
DB Structure :
{
    "username": {
        Pi = N                   # index of correct password
    },
}
"""


@app.route("/", methods=["GET"])
def home():
    return "HoneyWords Checker Server is running locally"


@app.route("/check_entry", methods=["POST"])
def check_entry():
    """
    Takes in username and Pi
    Returns if honeyword is detected
    """
    data = request.values
    username = data["username"]
    is_honeyword = None
    if username in honeywords_db.keys():
        Pi = honeywords_db[username]["Pi"]
        if int(data["Pi"]) != int(Pi):
            is_honeyword = True
            print("\nAlert: HoneyWord detected on user", username, "\n")
        else:
            is_honeyword = False
    return {"username": username,
            "is_honeyword": is_honeyword}


@app.route("/register_entry", methods=["POST"])
def register_entry():
    """
    Takes in username and Pi
    """
    data = request.values
    try:
        username = str(data["username"])
        honeywords_db[username] = {}
        Pi = int(data["Pi"])
        honeywords_db[username]["Pi"] = Pi
        dump_db_to_file(honeywords_db, args.db_name)
        status = "Entry recorded success"
    except Exception as e:
        status = "Error: "+str(e)
    return {"username": username,
            "status": status}


if __name__ == "__main__":
    app.run(port=9999)
