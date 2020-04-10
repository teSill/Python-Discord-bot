import tmdb_manager
import random
import discord
from trivia.trivia_manager import TriviaManager
import movie_data


async def ask_who_directed_movie(ctx):
    movie_id = None
    while movie_id is None:

        movie = tmdb_manager.TMDB.get_recommended_movie_by_title(random.choice(movie_data.generic_movies), 6.5)
        try:
            movie_id = movie.id
        except AttributeError:
            continue

    director = tmdb_manager.get_director(movie_id)
    all_directors = [director]
    for m in tmdb_manager.TMDB.get_3_recommended_movies(movie.title):
        all_directors.append(tmdb_manager.get_director(m.id))

    random.shuffle(all_directors)

    embedded_msg = discord.Embed(title=f"Which of these directors directed the movie {movie.title}?", description="",
                                 color=0x00ff00)

    options = {
        "A": all_directors[0],
        "B": all_directors[1],
        "C": all_directors[2],
        "D": all_directors[3]
    }

    for key, value in options.items():
        if value == director:
            correct_option = key.lower()
        embedded_msg.add_field(name='\u200b', value=f"{key}: {value}", inline=False)

    await TriviaManager.create_trivia_game(str(ctx.channel.id), correct_option)
    sent_message = await ctx.send(embed=embedded_msg)
    await TriviaManager.display_reactions(sent_message)