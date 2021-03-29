import json
import random
import hashlib


def load_db_from_file(db_path):
    with open(db_path, "rb") as f:
        db = json.load(f)
    return db


def dump_db_to_file(db, db_path):
    with open(db_path, "w") as outfile:
        json.dump(db, outfile)


def clean_inputs(text):
    clean_text = str(text).strip()
    return clean_text


def hash_text(text):
    hash_object = hashlib.sha256(text.encode("utf-8"))
    hashed = hash_object.hexdigest()
    return hashed


def generate_sweetwords(input_password, target_n=10, honeywords_file="./top_1000000_passwords.txt"):
    # source of common passwords file:
    # https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
    honeywords = [line.rstrip("\n") for line in open(honeywords_file)]
    sweetwords = [input_password]
    for i in range(target_n):
        j = random.randint(0, len(honeywords))
        honeyword = honeywords[j]
        if honeyword not in sweetwords:
            sweetwords.append(honeyword)
    sweetwords.append("demo_honeyword")
    random.shuffle(sweetwords)
    Pi = sweetwords.index(input_password)
    # hash everything
    sweetwords = [hash_text(s) for s in sweetwords]
    return {"sweetwords": sweetwords,
            "Pi": Pi}

