# PCG-Plus Bot
## Automated Pokemon Catcher for Pokemon Community Game (Twitch)
### Created By Damon Murdoch ([@SirScrubbington](https://github.com/SirScrubbington))

## Description

PCG-Plus is a Python bot designed to automate the process of catching Pokemon in the Pokemon Community Game on Twitch. It includes features such as automatic purchasing of Pokeballs, checking if a Pokemon is already in the Pokedex, and prioritizing catching favorite Pokemon. This bot interacts with Twitch chat and is customizable through environment variables.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Favorite Pokemon Features](#favorite-pokemon-features)
- [Environment Variables](#environment-variables)
- [Future Changes](#future-changes)
- [Problems / Improvements](#problems--improvements)
- [Changelog](#changelog)
- [Sponsor this Project](#sponsor-this-project)

## Installation

To install and run this bot:

1. Clone the repository:
   ```bash
   git clone https://github.com/damon-murdoch/pcg-plus
   cd PCG-Plus
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables in a `.env` file (refer to the [Environment Variables](#environment-variables) section for more details).

4. Run the bot:
   ```bash
   python pcgplus.py
   ```

## Usage

The bot listens for messages in the Twitch chat, automatically identifies wild Pokemon spawns, and catches them using a Pokeball. It can also check if the Pokemon is already in the Pokedex before catching it.

- **Automatic Catch**: The bot will use the specified Pokeball type to catch a Pokemon.
- **Check Pokedex**: If enabled, the bot will check whether the Pokemon is already in your Pokedex before attempting to catch it.

## Favorite Pokemon Features

This bot includes advanced features to help prioritize certain favorite Pokemon:

- **Favorite Pokemon**: You can specify a list of favorite Pokemon, and the bot will prioritize catching them, even if Pokedex checking is enabled.
- **Favorite Ball**: You can assign a different Pokeball to be used for favorite Pokemon.
- **Evolutions**: Optionally include any evolutions or previous forms of the favorite Pokemon in the priority list.
- **Favorite Only**: You can set the bot to only catch your favorite Pokemon, ignoring all others.

## Environment Variables

PCG-Plus uses a `.env` file to configure the bot. Below is an example of the `sample.env` file provided:

```env
# Account Properties
ACCESS_TOKEN=[my-access-token]
BOT_USERNAME=[my-bot-name]
BOT_CHANNEL=[my-connected-channel]

# General Config
CHECK_POKEDEX=false
BALL_TYPE=pokeball

# Favorite Pokemon
# FAV_TAGS=sublegendary,restrictedlegendary,mythical,ultrabeast,paradox
# FAV_POKEMON=ralts,zorua
# FAV_INCLUDE_EVOS=true
# FAV_INCLUDE_PREVO=true
# FAV_BALL_TYPE=greatball
```

Make sure to replace `[my-access-token]`, `[my-bot-name]`, and `[my-connected-channel]` with your actual Twitch bot credentials. You can customize various other settings, such as the Pokeball type and favorite Pokemon preferences.

## Future Changes

The following changes and improvements are planned for future updates:

### Change Table

| Change Description               | Priority |
| -------------------------------- | -------- |
| Implement more sophisticated ball purchase logic | Low     |

## Problems / Improvements

If you have any suggested improvements for this project or encounter any issues, please feel free to open an issue [here](../../issues) or send me a message on Twitter detailing the issue and how it can be replicated.

## Changelog

### Ver. 1.0.0

- Added features to catch favorite Pokemon, including special Pokeball options and evolution handling.

### Ver. 0.0.3

- Minor improvements

### Ver. 0.0.2

- Made functions for several reused messages / responses, implemented error handling for event_message for troubleshooting purposes

### Ver. 0.0.1

- Initial release with basic Pokemon catching functionality and Pokedex checking feature, as well as Docker support.

## Sponsor this Project

If you'd like to support this project and other future projects, please feel free to use the PayPal donation link below.  
[https://www.paypal.com/paypalme/sirsc](https://www.paypal.com/paypalme/sirsc)
