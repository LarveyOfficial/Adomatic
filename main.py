print("Bot Written By Larvey#0001")
import pymongo
import asyncio
import Config
import discord
import datetime
from discord.ext import commands
import logging
import random
import traceback

async def get_prefix(bot, message):
    return commands.when_mentioned_or("a!")(bot, message)


bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)

# Remove default help command
bot.remove_command("help")

# Cogs
cogs = ["ad"]

for cog in cogs:
    bot.load_extension("Cogs." + cog)


def owner(ctx):
    return int(ctx.author.id) in Config.OWNERIDS

@commands.check(owner)
async def restart(ctx):
    """
    Restart the bot.
    """
    restarting = discord.Embed(
        title = "Restarting...",
        color = Config.MAINCOLOR
    )
    msg = await ctx.send(embed = restarting)
    for cog in cogs:
        bot.reload_extension("Cogs." + cog)
        restarting.add_field(name = f"{cog}", value = "✅ Restarted!")
        await msg.edit(embed = restarting)
    restarting.title = "Bot Restarted"
    await msg.edit(embed = restarting)
    logging.info(f"Bot has been restarted succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users by {ctx.author.name}#{ctx.author.discriminator} (ID - {ctx.author.id})!")
    await msg.delete(delay = 3)
    if ctx.guild != None:
        await ctx.message.delete(delay = 3)



bot.run(Config.TOKEN)
