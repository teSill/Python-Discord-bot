import imdb_manager
import random
import discord
import movie_data
from trivia_manager import TriviaManager


class TriviaQuestions:
    @classmethod
    async def ask_for_release_year(cls, ctx, title):
        imdb_title = imdb_manager.search_movie(title)
        imdb_movie = imdb_manager.get_movie(imdb_title.getID())
        release_year = imdb_manager.get_year(imdb_movie)

        decoy_years = [release_year]
        for i in range(0, 3):
            rnd_num = random.randrange(release_year - 15, release_year + 15)
            decoy_years.append(rnd_num)

        embedded_msg = discord.Embed(title=f"Which year was '{title}' released in?", description="",
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
        await ctx.send(embed=embedded_msg)

#ask_for_director = 2
#ask_which_movie_these_actors_starred_in = 3
#ask_for_movie_show_plot = 4


async def ask_random_question(ctx):
    title = random.choice(movie_data.generic_movies)
    # decoy_movies = TMDB.get_3_recommended_movies(title)
    await TriviaQuestions.ask_for_release_year(ctx, title)
