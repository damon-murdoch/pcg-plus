import os
import time
import random

from dotenv import load_dotenv
from src.log import write_log

# Twitch Chat Bot Interface
from twitchio.ext import commands

# Software Version
VERSION = "0.0.3"

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


def random_delay():
    # Random delay of 3-6 seconds
    time.sleep(random.uniform(3, 6))


def parse_spawn(message):
    # Seperate the species name from the spawn message
    return message.split("a wild ")[1].split(" appears")[0]

def parse_registered(message):
    # Seperate species name from registered message
    return message.split(f"{USERNAME} ")[1].split(" registered")[0]


class Bot(commands.Bot):

    def __init__(self):

        # Initialise bot
        super().__init__(
            token=ACCESS_TOKEN, prefix="?", initial_channels=[CHANNEL]  # Unused
        )

        # Current encounter tracking variable
        self.current_species = None

        # Item was purchased by bot
        self.purchased_item = False

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

        if CHECK_POKEDEX:
            await self.check_species()
        else:
            await self.purchase_ball()

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

    async def purchase_ball(self):

        write_log(f"Buying ball {BALL_TYPE} ...")

        # Bot purchased the last item
        self.purchased_item = True

        # Buy a pokeball (Or ball desired)
        await self.send_message(f"!pokeshop {BALL_TYPE} 1")

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
                    species = parse_spawn(content).lower()
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
                    elif "registered in Pokédex" in content:

                        # Get checked species from the message
                        species = parse_registered(content)

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
