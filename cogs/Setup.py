import pymongo
import asyncio
import Config
import datetime
import discord
from discord.ext import commands, tasks
import logging
import Utils

class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def setup(self, ctx, *, channel:discord.TextChannel=None):
        if ctx.author.id not in Config.OWNERIDS:
            embed = discord.Embed(
                title = "ERROR",
                description = "You are not permited to use that command",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        else:
            if channel != None:
                docs = Config.SERVERS.find_one({"server_id" : ctx.guild.id})
                if docs == None:
                    Config.SERVERS.insert_one({"server_id" : ctx.guild.id, "ads" : channel.id})
                else:
                    Config.SERVERS.update_one({'server_id' : ctx.guild.id}, {"$set" : {"ads" : channel.id}})
                embed = discord.Embed(
                    title = "Success!",
                    description = "Your channel ad has been set!",
                    color = Config.MAINCOLOR
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "ERROR",
                    description = "Please give a proper Channel",
                    color = Config.ERRORCOLOR
                )
                await ctx.send(embed = embed)
