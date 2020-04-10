import tmdb_manager
import random
import discord
from trivia.trivia_manager import TriviaManager
import movie_data


async def ask_which_movie_person_directed(ctx):
    movie_id = None
    while movie_id is None:
        movie = tmdb_manager.TMDB.get_recommended_movie_by_title(random.choice(movie_data.generic_movies), 6.5)
        movie_id = movie.id

    director = tmdb_manager.get_director(movie.id)

    all_options = tmdb_manager.TMDB.get_3_recommended_movies(movie.title)
    all_options.append(movie)
    random.shuffle(all_options)

    embedded_msg = discord.Embed(title=f"Which of these movies did {director} direct?", description="",
                                 color=0x00ff00)

    options = {
        "A": all_options[0],
        "B": all_options[1],
        "C": all_options[2],
        "D": all_options[3]
    }

    for key, value in options.items():
        if tmdb_manager.get_director(value.id) == director:
            correct_option = key.lower()
        embedded_msg.add_field(name='\u200b', value=f"{key}: {value}", inline=False)

    await TriviaManager.create_trivia_game(str(ctx.channel.id), correct_option)
    sent_message = await ctx.send(embed=embedded_msg)
    await TriviaManager.display_reactions(sent_message)