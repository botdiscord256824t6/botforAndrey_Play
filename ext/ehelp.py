import asyncio
from itertools import groupby
from threading import Thread
from time import time
import discord
from discord.ext import commands
from .react import Pages, Message


class NewHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_command_help(self, command: commands.Command):
        e = discord.Embed(title=self.get_command_signature(
            command), decription=command.help or 'No help provided.' + (f'\nA part of the {command.cog_name} cog.' if command.cog_name else ''))
        e.set_footer(text=f'The bot prefix is {self.clean_prefix}')

        await self.context.send(embed=e)

    async def send_group_help(self, group: commands.Group):
        e = discord.Embed(title=group.qualified_name,
                          description=group.short_doc or 'No help provided.' + (f'\nA part of the {group.cog_name} cog.' if group.cog_name else ''))

        filtered = await self.filter_commands(group.commands, sort=True)

        if filtered:
            for command in filtered:
                e.add_field(name=self.get_command_signature(command),
                            value=command.short_doc or 'No help provided.')

        e.set_footer(text=f'The bot prefix is {self.clean_prefix}')

        await self.context.send(embed=e)

    async def send_cog_help(self, cog: commands.Cog):
        e = discord.Embed(title=cog.qualified_name,
                          description=cog.description or 'No help provided.')

        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        if filtered:
            for command in filtered:
                e.add_field(name=self.get_command_signature(command),
                            value=command.short_doc or 'No help provided.')

        await self.context.send(embed=e)

    async def send_bot_help(self, mapping: dict):
        bot: commands.Bot = self.context.bot
        embeds = []
        filtered = await self.filter_commands(mapping[None], sort=True)
        count = sum([bool(await self.filter_commands(cog_commands, sort=True)) for cog, cog_commands in mapping.items() if cog is not None]) + 1
        if filtered:
            embeds.append(discord.Embed(title=bot.user.name,
                                        description=bot.description))
            embeds[0].set_author(name=f'Page 1/{count}')

            names = []
            for i in filtered:
                if i.name not in names:
                    embeds[0].add_field(
                        name=self.get_command_signature(i), value=i.help)
                    names.append(i.name)
        for cog, cog_commands in mapping.items():
            if cog is None:
                continue
            filtered = await self.filter_commands(cog_commands, sort=True)
            names = []
            print(names)

            if filtered:
                embeds.append(discord.Embed(title=cog.qualified_name,
                                            description=cog.description))
                embeds[-1].set_author(name=f'Page {len(embeds)}/{count}')

                for command in filtered:
                    if command.name not in names:
                        embeds[-1].add_field(name=self.get_command_signature(command),
                                             value=command.short_doc or 'No help provided.')
                        names.append(command.name)

        pages = Pages(self.context, [Message(embed=e) for e in embeds], 30.0)

        await pages.start()


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = NewHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))