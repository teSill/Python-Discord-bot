import random
import discord
from trivia.trivia_manager import TriviaManager
from user_data import UserData

from trivia.questions.what_release_year import ask_for_release_year
from trivia.questions.directed_which_movie import ask_which_movie_person_directed
from trivia.questions.who_directed_movie import ask_who_directed_movie

# ask_for_director = 2
# ask_which_movie_these_actors_starred_in = 3
# ask_for_movie_show_plot = 4


async def ask_random_question(ctx):
    questions = [ask_which_movie_person_directed(ctx), ask_for_release_year(ctx),
                 ask_who_directed_movie(ctx)]
    await random.choice(questions)


async def verify_guess(reaction, user):
    channel = reaction.message.channel
    if TriviaManager.channel_has_running_game(str(channel.id)):
        if not TriviaManager.user_can_guess(str(channel.id), str(user)):
            return

        trivia_emojis = ("🇦", "🇧", "🇨", "🇩")
        if reaction.emoji not in trivia_emojis:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        correct_option = TriviaManager.get_correct_answer(str(channel.id))

        options = {
            "a": trivia_emojis[0],
            "b": trivia_emojis[1],
            "c": trivia_emojis[2],
            "d": trivia_emojis[3],
        }

        for key, value in options.items():
            if reaction.emoji == value:
                if key == correct_option:
                    msg = f"{user} guessed the correct answer, {key.upper()}! Congratulations! " \
                          f"They've received 10 experience."
                    TriviaManager.clear_trivia_game(channel.id)
                    user = UserData(str(user))
                    user.add_experience(10)
                else:
                    msg = f"{user} guessed {key.upper()}. Wrong answer!"
                    TriviaManager.add_user_to_failed_attempts(str(channel.id), str(user))
                break

        embedded_msg = discord.Embed(title=msg, description="",
                                     color=0x00ff00)

        await channel.send(embed=embedded_msg)
