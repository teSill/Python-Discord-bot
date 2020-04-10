import imdb_manager
import random
import discord
import movie_data
from trivia_manager import TriviaManager
from tmdb_manager import TMDB
from user_data import UserData
import globals


class TriviaQuestions:
    @classmethod
    async def ask_for_release_year(cls, ctx):
        release_year = None
        while release_year is None:
            movie = TMDB.get_recommended_movie_by_title(random.choice(movie_data.generic_movies), 6.5)
            globals.latest_movie_query = movie
            release_year = int(str(movie.release_date).split("-")[0])

        decoy_years = [release_year]
        for i in range(0, 3):
            rnd_num = random.randrange(release_year - 15, release_year + 15)
            decoy_years.append(rnd_num)
        random.shuffle(decoy_years)

        embedded_msg = discord.Embed(title=f"Which year was '{movie.title}' released in?", description="",
                                     color=0x00ff00)

        decoy_years = [release_year]
        while len(decoy_years) < 4:
            rnd_num = random.randrange(release_year - 15, release_year + 15) if release_year <= 2005 \
                                        else random.randrange(release_year - 20, release_year)
            if rnd_num in decoy_years:
                continue
            decoy_years.append(rnd_num)

        random.shuffle(decoy_years)

        options = {
            "A": decoy_years[0],
            "B": decoy_years[1],
            "C": decoy_years[2],
            "D": decoy_years[3]
        }

        for key, value in options.items():
            if value == release_year:
                correct_option = key.lower()
            embedded_msg.add_field(name='\u200b', value=f"{key}: {value}", inline=False)

        await TriviaManager.create_trivia_game(str(ctx.channel.id), correct_option)
        sent_message = await ctx.send(embed=embedded_msg)
        await display_reactions(sent_message)

#ask_for_director = 2
#ask_which_movie_these_actors_starred_in = 3
#ask_for_movie_show_plot = 4


async def display_reactions(msg):
    await msg.add_reaction("🇦")
    await msg.add_reaction("🇧")
    await msg.add_reaction("🇨")
    await msg.add_reaction("🇩")


async def ask_random_question(ctx):
    # decoy_movies = TMDB.get_3_recommended_movies(title)
    await TriviaQuestions.ask_for_release_year(ctx)


async def verify_guess(reaction, user):
    channel = reaction.message.channel
    if TriviaManager.channel_has_running_game(str(channel.id)):
        if not TriviaManager.user_can_guess(str(channel.id), str(user)):
            return

        trivia_emojis = ["🇦", "🇧", "🇨", "🇩"]
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
