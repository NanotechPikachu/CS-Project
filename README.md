# CS Project - Discord Bot (Python)

This is the repo for the **Computer Science Project** for CBSE Board class 12.

This repo consists of a `main.py` file which consists of all functions and classes for the Discord Bot to work. 

## Discord Bot

The Discord Bot made by me uses the "JIKAN API" (an unofficial MyAnimeList API) to get anime information and displays some part of it in form of a Discord Embed. 

### Modules / Technologies Used

- This project uses the UI of Discord for the commanding of Bot. 
- A MySQL DataBase is used for storing the favorite anime of each user.
- Uses `discord.py` library for interacting with Discord API.
- Uses `jikanpy-v4` package to simplify the API request's programming to the JIKAN API (v4).
- Uses `mysql-connector` for connecting with the MySQL remote DataBase.

### Features

- Search for anime using name
- Has 'Next' and 'Prev' button to browse through the result set seamlessly 
- MySQL DataBase integration for storing favorite anime
- Get specific user's favorites list by command 

### Commands

This Bot only has three commands (Prefix - !!)

- `anime` - To search for anime. **Syntax:** `!!anime [anime_name]`
- `favorites` - To get a user's favorites list. **Syntax:** `!!favorites`. Alias - `fav`
- `ping` - To check if Bot is working. **Syntax:** `!!ping`