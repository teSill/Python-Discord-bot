# Temflix Discord Bot

Temflix is a simple movie bot written in Python that can be added to any discord server with minimal permissions. 
With it, you can search for detailed information on movies, save them to your watchlist, get movie recommendations based on movies you've saved, play movie trivia and much more.

To add this bot to your own server, go to:

https://discordapp.com/api/oauth2/authorize?client_id=695951529659727916&permissions=387136&scope=bot

The server may or may not stay online, but I'll gladly host it upon request.

### Prerequisites

* Python 3
* Personal TMDb API key (optional but some features won't work without it as they currently are). This is (currently) automatically given to you upon request on their website after registration.
* Discord application and your bots' token saved as an environment variable (by default as 'DISCORD_TOKEN')

## Getting Started

After getting the prerequisite, simply download the package, plug it in the IDE of your choosing and run the main file, 'temflix.py'. 

## Built With

* Python 3
* discord.py
* IMDbPY
* tmdbv3api

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
