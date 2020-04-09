import errno
import glob
import json
import os
import shutil
import random
from imdb import IMDb

trivia_dir = "./trivia_games"
trivia_questions_dir = "./trivia_questions/questions.json"
max_game_runtime = 120

ia = IMDb()


class TriviaManager:

    @classmethod
    def trivia_game_exists(cls, channel_id):
        for filename in glob.iglob(f"{trivia_dir}/*", recursive=True):
            if channel_id in filename:
                return True
        return False

    @classmethod
    def get_random_question(cls):
        with open(trivia_questions_dir, "r+") as f:
            data = json.load(f)
            random_question = random.choice(list(data["best_picture_questions"]))
            return random_question

    @classmethod
    def get_correct_answer(cls, channel_id):
        if not TriviaManager.trivia_game_exists(channel_id):
            print("Channel doesn't have a running trivia game.")
            return None

        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "r+") as f:
            data = json.load(f)
            return data

    @classmethod
    async def create_trivia_game(cls, channel_id, correct_answer):
        if TriviaManager.trivia_game_exists(channel_id):
            return

        with open(os.path.join(trivia_dir, f"{channel_id}.json"), "w") as f:
            json.dump(correct_answer, f, ensure_ascii=False, indent=4)

        # await asyncio.sleep(max_game_runtime)
        # print(f"Waited {max_game_runtime}s, let's delete the trivia game.")
        # TriviaManager.clear_trivia_game(channel_id)

    @classmethod
    def clear_trivia_game(cls, channel_id):
        path = os.path.join(trivia_dir, f"{channel_id}.json")
        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def create_trivia_folder(cls):
        try:
            os.mkdir(trivia_dir)
        except FileExistsError:
            print("Trivia games folder already exists...?")

    @classmethod
    def clear_trivia_folder(cls):
        try:
            shutil.rmtree(trivia_dir, ignore_errors=False, onerror=TriviaManager.on_error)
        except FileNotFoundError:
            print("Folder doesn't exist.")

    @classmethod
    def on_error(cls, path, exc):
        excvalue = exc[1]
        if cls in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            # change the file to be readable,writable,executable: 0777
            os.chmod(path, os.stat.S_IRWXU | os.stat.S_IRWXG | os.stat.S_IRWXO)
            # retry
            cls(path)
        else:
            print("hä")
