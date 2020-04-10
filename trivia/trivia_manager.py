import errno
import glob
import json
import os
import random
import shutil

from imdb import IMDb

trivia_dir = "trivia/trivia_active_games"
max_game_runtime = 120

ia = IMDb()


class TriviaManager:

    @classmethod
    def channel_has_running_game(cls, channel_id):
        for filename in glob.iglob(f"{trivia_dir}/*", recursive=True):
            if channel_id in filename:
                return True
        return False

    @classmethod
    def get_correct_answer(cls, channel_id):
        if not TriviaManager.channel_has_running_game(channel_id):
            print("Channel doesn't have a running trivia game.")
            return None

        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "r+") as f:
            data = json.load(f)
            return data.get("correct_answer")

    @classmethod
    def add_user_to_failed_attempts(cls, channel_id, user):
        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "r+") as f:
            data = json.load(f)
            users = data["wrong_guesses"]
            users.append(user)

        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "r+") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def user_can_guess(cls, channel_id, user):
        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "r+") as f:
            data = json.load(f)
            return user not in data["wrong_guesses"]

    @classmethod
    async def create_trivia_game(cls, channel_id, correct_answer):
        obj = {
            "correct_answer": correct_answer,
            "wrong_guesses": []
        }

        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "w") as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)

        # await asyncio.sleep(max_game_runtime)
        # print(f"Waited {max_game_runtime}s, let's delete the trivia game.")
        # TriviaManager.clear_trivia_game(channel_id)

    @classmethod
    def clear_trivia_game(cls, channel_id):
        path = os.path.join(trivia_dir, f"{channel_id}.json")
        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def clear_trivia_folder(cls):
        try:
            shutil.rmtree(trivia_dir, ignore_errors=True)
        except FileNotFoundError:
            print(f"{trivia_dir} doesn't exist.")

    @classmethod
    async def display_reactions(cls, msg):
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        await msg.add_reaction("🇨")
        await msg.add_reaction("🇩")
