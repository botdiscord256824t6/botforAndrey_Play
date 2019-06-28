import asyncio
from typing import List, Optional, Union
from collections import OrderedDict
import discord
from discord.ext import commands


class ReAct:
    def __init__(self, ctx, message, timeout: Optional[float] = None, remove: bool = True):
        self.remove = remove
        self.timeout = timeout
        self.reactions = OrderedDict()
        self.ctx = ctx
        self.bot: commands.Bot = ctx.bot
        self.message: discord.Message = message

    async def on_reaction(self, ctx):
        pass

    def reaction(self, emoji):
        # if emoji:
        def wrapper(func, emoji=emoji):
            self.reactions[emoji] = func
            return func
        # else:
            # def wrapper(func):
            #self.on_reaction = func
            # return func
        return wrapper

    async def terminate(self):
        return await self.message.clear_reactions()

    async def start(self):
        def check(payload: discord.RawReactionActionEvent):
            return payload.user_id == self.ctx.author.id and payload.emoji.name in list(self.reactions.keys()) and payload.message_id == self.message.id
        for i in self.reactions:
            await self.message.add_reaction(i)
        while True:
            try:
                r: discord.RawReactionActionEvent = (await self.bot.wait_for('raw_reaction_add', timeout=self.timeout, check=check))
            except asyncio.TimeoutError:
                return await self.terminate()
            try:
                await self.reactions[r.emoji.name](self.ctx)
            except:
                await self.terminate()
                raise
            if self.remove:
                await self.message.remove_reaction(r.emoji, self.ctx.author)


class Message(dict):
    def __init__(self, content: Optional[str] = None, embed: Optional[discord.Embed] = None):
        dict.__init__(self, content=content, embed=embed)


class Pages:
    def __init__(self, ctx, messages: List[Message], timeout: Optional[float] = None):
        self.page = 0
        self.pages = messages
        self.ctx = ctx
        self.timeout = timeout

    async def show_page(self, page):
        self.page = page
        await self.message.edit(**self.pages[page])

    async def start(self):
        self.message = await self.ctx.send(**self.pages[0])
        message = self.message
        react = ReAct(self.ctx, message, self.timeout)
        self.react = react

        # @react.reaction()
        # async def update(ctx):
        # await ctx.message.edit(**self.pages[self.page])

        @react.reaction('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
        async def first(ctx):
            '''goes to the first page'''
            await self.show_page(0)

        @react.reaction('\N{BLACK LEFT-POINTING TRIANGLE}')
        async def previous(ctx):
            '''goes to the previous page'''
            await self.show_page((self.page + len(self.pages) - 1)
                                 % len(self.pages))

        @react.reaction('\N{BLACK RIGHT-POINTING TRIANGLE}')
        async def next(ctx):
            '''goes to the next page'''
            await self.show_page((self.page + 1) % len(self.pages))

        @react.reaction('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
        async def last(ctx):
            '''goes to the last page'''
            await self.show_page(len(self.pages) - 1)

        @react.reaction('\N{INPUT SYMBOL FOR NUMBERS}')
        async def goto(ctx):
            '''lets you type a page number to go to'''
            try:
                await self.show_page(int((await ctx.bot.wait_for('message', timeout=self.timeout, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())).content) - 1)
            except TimeoutError:
                await ctx.send('Took too long.')
                await react.terminate()

        @react.reaction('\N{BLACK SQUARE FOR STOP}')
        async def stop(ctx):
            '''stops the interactive pagination session'''
            await react.terminate()

        @react.reaction('\N{INFORMATION SOURCE}')
        async def info(ctx):
            '''shows this message'''
            e = discord.Embed(title='What are these reactions for?', description='\n'.join([f'{r} {f.__doc__}' for r, f in react.reactions.items()]))
            await message.edit(embed=e)

        @react.reaction('\N{WHITE QUESTION MARK ORNAMENT}')
        async def help(ctx):
            e = discord.Embed(title='Bot signature',
                              description='__**You do not type in the brackets!**__')
            e.add_field(name='<argument>',
                        value='This means the `argument` is __**required**__.', inline=False)
            e.add_field(name='[argument]',
                        value='This means the `argument` is __**optional**__.', inline=False)
            e.add_field(name='[A|B]',
                        value='This means the it can be __**either `A` or `B`**__.', inline=False)
            e.add_field(name='[argument...]',
                        value='This means you can have multiple arguments.', inline=False)
            await message.edit(embed=e)

        await react.start()