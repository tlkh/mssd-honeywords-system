import json
import random
from flask import *
import argparse
import requests
from utils import *


parser = argparse.ArgumentParser()
parser.add_argument("--db_name", type=str, default="user_db.json")
parser.add_argument("--honeywords_server", type=str,
                    default="http://localhost:9999")
args = parser.parse_args()
app = Flask("web_server")

try:
    print("Loading user DB")
    user_db = load_db_from_file(args.db_name)
except Exception as e:
    print("Error:", e, "creating new user DB...")
    user_db = {}
    dump_db_to_file(user_db, args.db_name)
    print("New user DB is at args.db_name")

"""
Database structure:
{
    "username": {
        "sweetwords": []
    }
}
"""

def gen_response_page(display_text):
    pre = "<h1>Web Application</h1><p>"
    post = "</p><hr><a href='/'>Back to main page</a>"
    return pre+display_text+post


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("login.html")

    username = clean_inputs(request.form["username"])
    password = clean_inputs(request.form["password"])
    password = hash_text(password)

    if username not in user_db.keys():
        return gen_response_page("User does not exist")

    sweetwords = user_db[username]["sweetwords"]
    if password in sweetwords:
        Pi = sweetwords.index(password)
        request_url = args.honeywords_server+"/check_entry"
        honeyword_check = requests.post(request_url, data={
            "username": username,
            "Pi": Pi
        }).json()
        if honeyword_check["is_honeyword"] == True:
            print("\nAlert: HoneyWord detected on user", username, "\n")
            return gen_response_page("Invalid login credentials (hidden: honeyword alarm trigger)")
        else:
            return gen_response_page("Login success")
    else:
        return gen_response_page("Invalid login credentials")


@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template("register_user.html")

    username = clean_inputs(request.form["username"])
    password = clean_inputs(request.form["password"])

    sweetwords_data = generate_sweetwords(password, target_n=10)

    user_db[username] = {
        "sweetwords": sweetwords_data["sweetwords"],
    }

    Pi = sweetwords_data["Pi"]
    request_url = args.honeywords_server+"/register_entry"
    register_data = requests.post(request_url, data={
        "username": username,
        "Pi": Pi
    }).json()
    if register_data["status"] == "Entry recorded success":
        dump_db_to_file(user_db, args.db_name)
        return gen_response_page("Registration success")
    else:
        return gen_response_page("Registration Error: "+register_data["status"])


if __name__ == "__main__":
    app.run()
