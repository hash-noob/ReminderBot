import os
import discord
import asyncio
from discord.ext import commands,tasks
from dotenv import load_dotenv
from contest import upcomingContest

#scheduler if the event is today
async def schedule(time_str,event):
    total_seconds = 0
    parts = time_str.split(', ')
    for part in parts:
        value, unit = part.split()
        value = int(value)

        if unit.startswith('hr'):
            total_seconds += value * 3600
        elif unit.startswith('min'): 
            total_seconds += value * 60
        elif unit.startswith('sec'): 
            total_seconds += value
    
    total_seconds-=(60*60)
    print("task scheduled")
    print(event.title+" "+time_str+" "+str(total_seconds))
    await asyncio.sleep(total_seconds)
    await alert(event)
    print("scheduled task executed")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
Cid=int(os.getenv('CHANNEL_ID'))
C1=int(os.getenv('C1'))
C2=int(os.getenv('C2'))

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())


    
@bot.command(name='contest')
async def helper(ctx):
    upcomingContests,ongoingContests = upcomingContest()
    msg=''
    if len(ongoingContests)>0:
        msg+="Ongoing Contest\n"
        for contest in ongoingContests:
            s = [attr+" : "+getattr(contest, attr) for attr in vars(contest)]
            msg+= "\n".join(s)
            msg+="\n"+"-"*50+"\n"

    msg+="Upcoming Contests\n"
    for contest in upcomingContests:
        s = [attr+" : "+getattr(contest, attr) for attr in vars(contest)]
        msg+= "\n".join(s)
        msg+="\n"+"-"*50+"\n"
        
    await ctx.send(msg)

@tasks.loop(seconds=(12*60*60))
async def scheduler():
    print("task fired")
    contests,t = upcomingContest() #since we only schedule upcoming contests we are ignoring ongoing events with t
    for contest in contests:
        if "day" not in contest.starts_in:
            await schedule(contest.starts_in,contest)    

async def alert(contest):
    msg='@everyone\n'
    contest.starts_in =" 60 mins"
    s = [attr+" : "+getattr(contest, attr) for attr in vars(contest)]
    msg+= "\n".join(s)
    msg+="\n"+"-"*50+"\n"
    channel1 = bot.get_channel(C1)
    channel2 = bot.get_channel(C2)
    
    await channel1.send(msg)
    await channel2.send(msg)

@bot.event
async def on_ready():
    scheduler.start()
    print('Bot has connected to Discord!')
   
bot.run(TOKEN)
