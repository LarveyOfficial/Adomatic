import pymongo
import asyncio
import Config
import discord
import datetime
from discord.ext import commands, tasks
import logging
import Utils


class Ad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.send_ads = False
        self.cycle.start()

    def cog_unload(self):
        self.cycle.cancel()

    def owner(ctx):
        return int(ctx.author.id) in Config.OWNERIDS


    @tasks.loop(seconds = 10800)
    async def cycle(self):
        if self.send_ads:
            ad = Config.ADS.find_one({'index': self.index})
            if ad is not None and self.index > 0:
                adMessage = ad['ad']
                if 'ads' in server.keys():
                    guild = self.bot.get_guild(server['server_id'])
                    if guild is not None:
                        channel = guild.get_channel(server['ads'])
                        if channel is not None:
                            embed = discord.Embed(
                                title = "**Ad**",
                                description = adMessage,
                                color = Config.MAINCOLOR
                            )
                            embed.set_footer(text="Ad " + str(self.index) + " of " + str(Config.ADS.count_documents({})))
                            await channel.send(embed = embed)
                if self.index >= Config.ADS.count_documents({}):
                    self.index = 1
                else:
                    self.index += 1
            else:
                if self.index >= Config.ADS.count_documents({}):
                    self.index = 1
                else:
                    self.index += 1

    @cycle.before_loop
    async def before_cycle(self):
        time = ""
        with open('interval.txt', 'r+') as fp:
            time = fp.read()
        i = 0
        seconds = 0
        minutes = 0
        hours = 0
        for char in time.lower():
            if char == "s":
                if i > 1 and self.is_int(time[i-2:i]):
                    seconds = int(time[i-2:i])
                elif i > 0 and self.is_int(time[i-1]):
                    seconds = int(time[i-1])
                else:
                    continue
            elif char == "m":
                if i > 1 and self.is_int(time[i-2:i]):
                    minutes = int(time[i-2:i])
                elif i > 0 and self.is_int(time[i-1]):
                    minutes = int(time[i-1])
                else:
                    continue
            elif char == "h":
                if i > 1 and self.is_int(time[i-2:i]):
                    hours = int(time[i-2:i])
                elif i > 0 and self.is_int(time[i-1]):
                    hours = int(time[i-1])
                else:
                    continue
            i += 1

        if not (seconds == 0 and minutes == 0 and hours == 0):
            self.cycle.change_interval(seconds=seconds, minutes=minutes, hours=hours)

    @commands.group(aliases = ["ad"])
    @commands.check(owner)
    async def ads(self, ctx):
        if ctx.invoked_subcommand is None:
            state = ""
            if self.send_ads:
                state = "on"
            else:
                state = "off"
            embed = discord.Embed(
                title = f"Automatic Ads (currently toggled {state})",
                description = "`n!ads add <Text>` - Adds an ad to the list of ads\n`n!ads list` - Lists all the ads\n`n!ads remove <Ad index>` - Removes an ad from the list.\n`n!ads interval <0h0m0s>` - Changes time for Next run of Ads\n`n!ads toggle` - Toggle on or off Ads",
                color = Config.MAINCOLOR
            )
            await ctx.send(embed = embed)

    @ad.command(aliases = ['create'])
    async def add(self, ctx, *, theAd:str=None):
        if theAd == None:
            embed = discord.Embed(
                title = "Ad ERROR",
                description = "Please specify the text for the ad",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        else:
            documentnum = Config.ADS.count_documents({})
            Config.ADS.insert_one({"ad": theAd, "index": documentnum + 1})
            embed = discord.Embed(
                title = "Ads",
                description = "```" + theAd + "```\n\n**Ad has been added to the Ad List**",
                color = Config.MAINCOLOR
            )
            await ctx.send(embed = embed)

    @ad.command()
    async def toggle(self, ctx):
        self.send_ads = not self.send_ads
        state = ""
        if self.send_ads:
            state = "On"
        else:
            state = "Off"
        embed = discord.Embed(
            title="Ads",
            description=f"Toggled automatic ads {state}!",
            color=Config.MAINCOLOR
        )
        await ctx.send(embed=embed)

    def is_int(self, input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True

    @ad.command()
    async def interval(self, ctx, *, time:str=None):
        if time is None:
            embed = discord.Embed(
                title = "ERROR",
                description = "Please Provide a Time. e.g. `n!ads interval 1h3m3s`",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        else:
            i = 0
            seconds = 0
            minutes = 0
            hours = 0
            for char in time.lower():
                if char == "s":
                    if i > 1 and self.is_int(time[i-2:i]):
                        seconds = int(time[i-2:i])
                    elif i > 0 and self.is_int(time[i-1]):
                        seconds = int(time[i-1])
                    else:
                        continue
                elif char == "m":
                    if i > 1 and self.is_int(time[i-2:i]):
                        minutes = int(time[i-2:i])
                    elif i > 0 and self.is_int(time[i-1]):
                        minutes = int(time[i-1])
                    else:
                        continue
                elif char == "h":
                    if i > 1 and self.is_int(time[i-2:i]):
                        hours = int(time[i-2:i])
                    elif i > 0 and self.is_int(time[i-1]):
                        hours = int(time[i-1])
                    else:
                        continue
                i += 1

            if seconds == 0 and minutes == 0 and hours == 0:
                embed = discord.Embed(
                    title = "ERROR",
                    description = "Please Provide a Time. e.g. `n!ads interval 1h30m30s`",
                    color = Config.ERRORCOLOR
                )
                await ctx.send(embed = embed)
            else:
                self.cycle.change_interval(seconds=seconds, minutes=minutes, hours=hours)
                embed = discord.Embed(
                    title = "Interval",
                    description = f"Time has been changed to {hours}h{minutes}m{seconds}s",
                    color = Config.MAINCOLOR
                )
                await ctx.send(embed = embed)
                with open("interval.txt", 'w+') as fp:
                    fp.write(time)




    @ad.command()
    async def list(self, ctx):
        documentnum = Config.ADS.count_documents({})
        if documentnum == 0:
            embed = discord.Embed(
                title = "No Ads",
                description = "There are no ads in the ad list!",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        else:
            string = "__The Ad List:__ \n"
            for ad in Config.ADS.find({}):
                if len(ad['ad']) > 25:
                    string += "\n **[" + str(ad['index']) + "]** *" + ad['ad'][:25] + "...*"
                else:
                    string += "\n **[" + str(ad['index']) + "]** *" + ad['ad'] + "*"
            embed = discord.Embed(
                title = "Ad List",
                description = string,
                color = Config.MAINCOLOR
            )
            await ctx.send(embed = embed)
    @ad.command(aliases = ["remove"])
    async def delete(self, ctx, *, index:int=None):
        if index == None:
            embed = discord.Embed(
                title = "Ad ERROR",
                description = "Please specify an ad to delete",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        else:
            the_doc = Config.ADS.find_one({'index': index})
            if the_doc != None:
                Config.ADS.delete_one({'index': index})
                for ad in Config.ADS.find({}):
                    if ad['index'] > index:
                         Config.ADS.update_one({"index": ad['index']}, {"$set": {"index": ad['index'] - 1 }})
                embed = discord.Embed(
                    title = "Ads",
                    description = "Ad ["+str(index)+"] Deleted from The Ad List",
                    color = Config.MAINCOLOR
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "ERROR",
                    description = "That Ad Does not exist.",
                    color = Config.ERRORCOLOR
                )
                await ctx.send(embed = embed)



def setup(bot):
    bot.add_cog(Ad(bot))
