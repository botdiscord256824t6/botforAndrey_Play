import asyncio
import discord
from discord.ext import commands

from const import token


prefix = '%'
INITIAL_EXTENSIONS = [
    'ext.ehelp',
    'ext.mod',
    'ext.music'
]

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print('Бот был запущен с параметрами:')
    print('Имя бота:' + bot.user.name)
    print('ID бота:' + str(bot.user.id))
    print('------')


@bot.command(aliases=['plus'])
async def add(ctx, a: int, b: int):
    '''Adds `a` to `b`'''
    await ctx.send(a + b)


@bot.command(aliases=['multiply', 'umnozit'])
async def mult(ctx, a: int, b: int):
    '''Multiplies `a` and `b`'''
    await ctx.send(a * b)


@bot.command()
async def greet(ctx):
    '''Greets'''
    await ctx.send(":smiley: :wave: Hello, there!")


@bot.command()
async def cat(ctx):
    '''Sends a cat'''
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")


@bot.command()
async def bot_info(ctx):
    embed = discord.Embed(
        title=bot.user.name, description="Nicest bot there is ever.", color=0xeee657)
    embed.add_field(name="Authors", value="LeMIT and Mr_ChAI")
    embed.add_field(name="Guild count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Invite", value="https://discord.gg/5CHCJk2")
    await ctx.send(embed=embed)

for i in INITIAL_EXTENSIONS:
    bot.load_extension(i)

bot.run(token)