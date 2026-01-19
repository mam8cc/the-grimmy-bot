import os
from twitchio.ext import commands
from characters import ROLES
from dotenv import load_dotenv

load_dotenv()

twitch_token = os.environ["TOKEN"]
channels = os.environ["CHANNELS"].split(",")


# Setup state holders per channel for admin inputted commands
AMNE = {}
WIZARD = {}
YAG = {}
DJINN = {}
for channel in channels:
    AMNE[channel] = None
    YAG[channel] = None
    WIZARD[channel] = None
    DJINN[channel] = None

ALIASES = []

for role in ROLES:
    ALIASES = ALIASES + role.aliases()


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=twitch_token, prefix="!", initial_channels=channels)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    @commands.command()
    async def join(self, ctx: commands.Context):
        await ctx.reply(
            "Come play with us!  Join our Discord community!  https://join.thegrim.gg"
        )

    @commands.command()
    async def turfwar(self, ctx: commands.Context):
        await ctx.reply("Turf War v1.2 Rules => https://shorturl.at/djScA")

    @commands.command()
    async def setamne(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply("Only moderators can set the amnesiac ability.")
            return

        parts = ctx.message.content.split(" ", 1)
        if len(parts) < 2:
            await ctx.reply("Usage: !setamne <ability>")
            return

        AMNE[ctx.channel.name] = parts[1]

    @commands.command()
    async def amne(self, ctx: commands.Context):
        ability = AMNE[ctx.channel.name]

        if ability is None:
            ability = f"No ability has been set for the channel {ctx.channel.name}"

        await ctx.reply(f'The Amnesiac Ability Is: "{ability}"')

    @commands.command()
    async def setyag(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply("Only moderators can set the Yaggababble phrase.")
            return

        parts = ctx.message.content.split(" ", 1)
        if len(parts) < 2:
            await ctx.reply("Usage: !setyag <phrase>")
            return

        YAG[ctx.channel.name] = parts[1]

    @commands.command()
    async def yag(self, ctx: commands.Context):
        ability = YAG[ctx.channel.name]

        if ability is None:
            ability = f"No phrase has been set for the channel {ctx.channel.name}"

        await ctx.reply(f'The Yaggababble Phrase Is: "{ability}"')

    @commands.command()
    async def setwiz(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply("Only moderators can set the wizard ability.")
            return

        parts = ctx.message.content.split(" ", 1)
        if len(parts) < 2:
            await ctx.reply("Usage: !setwiz <ability>")
            return

        WIZARD[ctx.channel.name] = parts[1]

    @commands.command()
    async def wiz(self, ctx: commands.Context):
        ability = WIZARD[ctx.channel.name]

        if ability is None:
            ability = f"No ability has been set for the channel {ctx.channel.name}"

        await ctx.reply(f'The Wizard Wish Is: "{ability}"')

    @commands.command()
    async def setdjinn(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply("Only moderators can set the djinn rule.")
            return

        parts = ctx.message.content.split(" ", 1)
        if len(parts) < 2:
            await ctx.reply("Usage: !setdjinn <rule>")
            return

        DJINN[ctx.channel.name] = parts[1]

    @commands.command()
    async def djinnrule(self, ctx: commands.Context):
        rule = DJINN[ctx.channel.name]

        if rule is None:
            rule = f"No Djinn rule has been set for the channel {ctx.channel.name}"

        await ctx.reply(f'The Djinn Rule Is: "{rule}"')

    @commands.command(aliases=ALIASES)
    async def char(self, ctx: commands.Context):
        character = await self.find_character(ctx.message.content[1:])

        if character is None:
            await ctx.reply("Character not found. Check your spelling you goof!")
            return

        response = f"{character.name} ({str(character.type.value)}): {character.rule}"
        if character.link:
            response += f" Wiki: {character.link}"
        await ctx.reply(response)

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.reply("""
        !char, !amne, !yag, !wiz, !djinnrule, !turfwar, !join
    """)

    async def find_character(self, name: str):
        print(f"Trying to find {name}")
        for role in ROLES:
            name = name.lower()

            if name in role.aliases():
                return role

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)


bot = Bot()
bot.run()
