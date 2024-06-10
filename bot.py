import os
from twitchio.ext import commands
from characters import *
from dotenv import load_dotenv

load_dotenv()

twitch_token = os.environ['TOKEN']
channels = os.environ['CHANNELS'].split(',')


# Setup state holders per channel for admin inputted commands
AMNE = {}

YAG = {}

for channel in channels:
    AMNE[channel] = None
    YAG[channel] = None

ALIASES = []

for role in ROLES:
    ALIASES = ALIASES + role.aliases()


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=twitch_token, prefix='!', initial_channels=channels)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def join(self, ctx: commands.Context):
        await ctx.reply('Come play with us!  Join our Discord community!  https://join.thegrim.gg')

    @commands.command()
    async def turfwar(self, ctx: commands.Context):
        await ctx.reply('Turf War v1.2 Rules => https://shorturl.at/djScA')

    @commands.command()
    async def setamne(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply('Only moderators can set the amnesiac ability.')

        AMNE[ctx.channel.name] = ctx.message.content.split(' ', 1)[1]

    @commands.command()
    async def amne(self, ctx: commands.Context):
        ability = AMNE[ctx.channel.name]

        if ability is None:
            ability = f'No ability has been set for the channel {ctx.channel.name}'

        await ctx.reply(f'The Amnesiac Ability Is: "{ability}"')

    @commands.command()
    async def setyag(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply('Only moderators can set the Yaggababble phrase.')

        YAG[ctx.channel.name] = ctx.message.content.split(' ', 1)[1]

    @commands.command()
    async def yag(self, ctx: commands.Context):
        ability = YAG[ctx.channel.name]

        if ability is None:
            ability = f'No phrase has been set for the channel {ctx.channel.name}'

        await ctx.reply(f'The Yaggababble Phrase Is: "{ability}"')

    @commands.command(aliases=ALIASES)
    async def char(self, ctx: commands.Context):

        try:
            character = await self.find_character(ctx.message.content[1:])
        except IndexError:
            ctx.reply('Character not found.  Check your spelling you goof!')
            return

        await ctx.reply(f'''{character.name} ({str(character.type.value)}): {character.rule} Wiki: {character.link}
''')

    async def find_character(self, name: str):
        print(f'Trying to find {name}')
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