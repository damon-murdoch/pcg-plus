# PCG-Plus Bot
## Automated Pokemon Catcher for Pokemon Community Game (Twitch)
### Created By Damon Murdoch ([@SirScrubbington](https://github.com/SirScrubbington))

## Description

PCG-Plus is a Python bot designed to automate the process of catching Pokemon in the Pokemon Community Game on Twitch. It includes features such as automatic purchasing of Pokeballs and checking if a Pokemon is already in the Pokedex before attempting to catch it. This bot interacts with Twitch chat and is customizable through environment variables.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Future Changes](#future-changes)
- [Problems / Improvements](#problems--improvements)
- [Changelog](#changelog)
- [Sponsor this Project](#sponsor-this-project)

## Installation

To install and run this bot:

1. Clone the repository:
   ```bash
   git clone https://github.com/SirScrubbington/PCG-Plus.git
   cd PCG-Plus
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables in a `.env` file:
   ```env
   ACCESS_TOKEN=your_twitch_access_token
   BOT_USERNAME=your_bot_username
   BOT_CHANNEL=target_twitch_channel
   BALL_TYPE=pokeball
   CHECK_POKEDEX=false
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

The bot listens for messages in the Twitch chat, automatically identifies wild Pokemon spawns, and catches them using a Pokeball. It can also check if the Pokemon is already in the Pokedex before catching it.

- **Automatic Catch**: The bot will use the specified Pokeball type to catch a Pokemon.
- **Check Pokedex**: If enabled, the bot will check whether the Pokemon is already in your Pokedex before attempting to catch it.

## Future Changes

The following changes and improvements are planned for future updates:

### Change Table

| Change Description               | Priority |
| -------------------------------- | -------- |
| Implement more sophisticated ball purchase logic | Low     |

## Problems / Improvements

If you have any suggested improvements for this project or encounter any issues, please feel free to open an issue [here](../../issues) or send me a message on Twitter detailing the issue and how it can be replicated.

## Changelog

### Ver. 0.0.1

- Initial release with basic Pokemon catching functionality and Pokedex checking feature, as well as Docker support.

## Sponsor this Project

If you'd like to support this project and other future projects, please feel free to use the PayPal donation link below.  
[https://www.paypal.com/paypalme/sirsc](https://www.paypal.com/paypalme/sirsc)
