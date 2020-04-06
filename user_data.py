import glob
import os
import json
import operator
import functools

user_dir = "./users"

default_json_obj = {
        "UserData": [{
            "is_premium": False,
            "experience": 0,
            "level": 0
        }],
        "Watchlist": [{

        }]
    }


def user_save_exists(username):
    for filename in glob.iglob(f"{user_dir}/*", recursive=True):
        if username in filename:
            return True
    return False


def create_user_if_not_existing(username):
    for filename in glob.iglob(f"{user_dir}/*", recursive=True):
        if username in filename:
            return
    UserData(username)


class UserData:
    def __init__(self, username):
        self.username = username
        self.save_path = os.path.join(user_dir, f"{self.username}.json")
        self.create_user_save()
        self.is_premium = self.get_premium()
        self.experience = self.get_experience()
        self.level = self.get_level()
        self.watchlist = self.get_watchlist()
        self.max_watchlist_size = 50 if self.is_premium else 10

    def create_user_save(self):
        if not user_save_exists(self.username):
            with open(self.save_path, "w") as db_file:
                json.dump(default_json_obj, db_file, ensure_ascii=False, indent=4)

    async def add_to_save(self, data):
        with open(os.path.join(user_dir, f"{self.username}.json"), "w") as db_file:
            json.dump(data, db_file, ensure_ascii=False, indent=4)

    def get_premium(self):
        with open(self.save_path, "r+") as f:
            data = json.load(f)
            return data["UserData"][0].get("is_premium")

    def get_experience(self):
        with open(self.save_path, "r+") as f:
            data = json.load(f)
            return data["UserData"][0].get("experience")

    def get_level(self):
        with open(self.save_path, "r+") as f:
            data = json.load(f)
            return data["UserData"][0].get("level")

    def get_watchlist(self):
        with open(self.save_path, "r+") as f:
            data = json.load(f)
            return data["Watchlist"][0]

    @classmethod
    def get_new_user_instance_by_name(cls, username):
        return UserData(username)
