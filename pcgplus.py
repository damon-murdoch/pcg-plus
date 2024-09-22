import os
import time
import random

from dotenv import load_dotenv
from src.log import write_log

import src.showdown as showdown

# Twitch Chat Bot Interface
from twitchio.ext import commands

# Software Version
VERSION = "1.0.0"

# Pokemon Community Game Account
PCG_ID = "pokemoncommunitygame"

# Load vars from .env
load_dotenv()

# Load Environment Variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL = os.getenv("BOT_CHANNEL")

# Get the account username (force lowercase)
USERNAME = os.getenv("BOT_USERNAME").lower()

# Get the Pokeball type (Default: pokeball)
BALL_TYPE = os.getenv("BALL_TYPE", "pokeball")

# Check if the dex entry is registered before catching (Boolean)
CHECK_POKEDEX = bool(os.getenv("CHECK_POKEDEX", "false") == "true")

# Favorite Pokemon
# These will be re-caught, even if CHECK_POKEDEX is set to true
# and optionally can be caught with a different ball 'BALL_FAVORITES'

# List of favorite tags
FAV_TAGS = os.getenv("FAV_TAGS", "").split(",")

# List of custom favorite Pokemon
FAV_POKEMON = os.getenv("FAV_POKEMON", "").split(",")

# If this is set to true, any evolutions for the FAV_POKEMON category
# will be included, even if they are not explicitly provided.
FAV_INCLUDE_EVOS = bool(os.getenv("FAV_INCLUDE_EVOS", "false") == "true")

# If this is set to true, any previous evolutions for the FAV_POKEMON
# category will be included, even if they are not explicitly provided.
FAV_INCLUDE_PREVO = bool(os.getenv("FAV_INCLUDE_PREVO", "false") == "true")

# Get the ball to use for favorite Pokemon
# If not set, this will use the same ball as BALL_TYPE
FAV_BALL_TYPE = os.getenv("FAV_BALL", BALL_TYPE)

# If this is set to true, ONLY favorite Pokemon will be catched
FAV_ONLY = bool(os.getenv("FAV_ONLY", "false") == "true")


def random_delay():
    # Random delay of 3-6 seconds
    time.sleep(random.uniform(3, 6))


def parse_spawn(message):
    # Seperate the species name from the spawn message
    return message.split("a wild ")[1].split(" appears")[0]


def parse_registered(message):
    # Seperate species name from registered message
    return message.split(f"{USERNAME} ")[1].split(" registered")[0]


def parse_showdown(species):
    # Convert to lowercase and remove dashes / spaces
    return species.lower().replace("-", "").replace(" ", "")


class Bot(commands.Bot):

    def __init__(self):

        # Initialise bot
        super().__init__(
            token=ACCESS_TOKEN, prefix="?", initial_channels=[CHANNEL]  # Unused
        )

        # Import the showdown data and save as moves, dex
        self.moves, self.dex = showdown.get_showdown_data()

        # Current encounter tracking variable
        self.current_species = None

        # Item was purchased by bot
        self.purchased_item = False

    def is_favorite(self, species):

        # Species is a favorite
        if species in FAV_POKEMON:
            return True

        # Get the data for the species
        data = self.dex[species]

        # Check for fav. tags
        if FAV_TAGS and "tags" in data:
            for tag in data["tags"]:
                if parse_showdown(tag) in FAV_TAGS:
                    return True  # Tag is favorite

        # Check for fav. evolutions
        if FAV_INCLUDE_EVOS and "evos" in data:
            for evo in data["evos"]:
                if parse_showdown(evo) in FAV_POKEMON:
                    return True  # Evo is favorite

        # Check for fav. previous evolutions
        if FAV_INCLUDE_PREVO and "prevo" in data:
            if parse_showdown(data["prevo"]) in FAV_POKEMON:
                return True  # Prevo is favorite

        # Not favorite
        return False

    async def send_message(self, message, delay=True):

        # Wait for random delay
        if delay:
            random_delay()

        # Send the message to the channel
        await self.connected_channels[0].send(message)

    async def check_species(self):

        write_log("Checking for Pokedex entry ...")

        # Send pokecheck request
        await self.send_message(f"!pokecheck")

    async def found_pokemon(self, species):

        write_log(f"Pokemon found: {species}")

        # Parse the species from the message
        self.current_species = species

        # If the species is a favorite
        if self.is_favorite(species):
            await self.purchase_ball(favorite=True)
        else:
            if FAV_ONLY:
                write_log(f"Pokemon {species} is not a favorite, ignoring ...")
            if CHECK_POKEDEX:
                await self.check_species()
            else:
                await self.purchase_ball(favorite=False)

    async def catch_pokemon(self):

        write_log(f"Catching Pokemon {self.current_species} ...")

        # Attempt to catch the Pokemon
        await self.send_message(f"!pokecatch {BALL_TYPE}")

    async def catch_complete(self, success=True):
        # Current species found
        if self.current_species:
            if success:
                write_log(f"Pokemon {self.current_species} caught successfully!")
            else:
                write_log(f"Pokemon {self.current_species} was not caught.")
        self.current_species = None

    async def purchase_ball(self, favorite: bool = False):

        # Select ball type
        ball = BALL_TYPE
        if favorite:
            ball = FAV_BALL_TYPE

        write_log(f"Buying ball {ball} ...")

        # Bot purchased the last item
        self.purchased_item = True

        # Buy a pokeball (Or ball desired)
        await self.send_message(f"!pokeshop {ball} 1")

    async def event_ready(self):
        write_log(f"Bot started! Username: {USERNAME} ...")

    async def event_message(self, message):

        try:

            # Ignore own messages
            if message.echo:
                return

            # Get message author
            author = message.author

            # Community game message
            if author.name == PCG_ID:

                # Parse message content (Lowercase)
                content = message.content.lower()

                # If the message is a wild Pokemon
                if "catch it using !pokecatch" in content:
                    species = parse_showdown(parse_spawn(content))
                    await self.found_pokemon(species)

                # TODO: Support more commands

                # If this account is tagged
                elif f"@{USERNAME}" in content:

                    # Item purchase successful
                    if "purchase successful!" in content:
                        # Bot purchased a ball
                        if self.purchased_item == True:
                            write_log(f"Ball {BALL_TYPE} purchased successfully!")
                            # Species available
                            if self.current_species:
                                # Attempt to catch the Pokemon
                                await self.catch_pokemon()
                            # Mark ball purchased as false
                            self.purchased_item = False

                    # Pokecheck message response
                    elif "registered in" in content:

                        # Get checked species from the message
                        species = parse_showdown(parse_registered(content))

                        # Bot catching Pokemon
                        if self.current_species == species:
                            write_log(f"Species {self.current_species} not registered!")
                            await self.purchase_ball()

                    # Captured Pokemon successfully
                    elif "has been caught by" in content:
                        await self.catch_complete(True)

                    # TODO: Support more commands

                # Player failed to catch
                elif "has been caught by" in content:
                    await self.catch_complete(False)

                # Nobody caught
                elif "no one caught it" in content:
                    await self.catch_complete(False)
            # Ignore messages by others
        except Exception as e:
            write_log(f"Failed to handle message event! {e}")


if __name__ == "__main__":

    write_log(f"Starting PCG-Plus v{VERSION} ...")

    # Create bot
    bot = Bot()

    # Start bot
    bot.run()
