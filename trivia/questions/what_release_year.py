import random
import tmdb_manager
import movie_data
import discord
import globals
from trivia.trivia_manager import TriviaManager


async def ask_for_release_year(ctx):
    release_year = None
    while release_year is None:
        movie = tmdb_manager.TMDB.get_recommended_movie_by_title(random.choice(movie_data.generic_movies), 6.5)
        try:
            release_year = int(str(movie.release_date).split("-")[0])
        except AttributeError:
            continue
        globals.latest_movie_query = movie

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
    await TriviaManager.display_reactions(sent_message)