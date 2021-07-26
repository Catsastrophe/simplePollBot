from discord import *
from discord.ext import commands
import json, emoji, sys

class BreakIt(Exception): pass


config = json.load(open('config.json'))
token = config.get("Discord Token")
command_prefix = str(config.get("Command Prefix"))
channel_id = int(config.get("channel"))
poll_maker_id = int(config.get("poll maker id"))

client = commands.Bot(command_prefix = command_prefix, intents = Intents(messages = True, guilds = True, reactions = True))

client.remove_command('help')

@client.event
async def on_ready():
    print("Bot ready", sys.version)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        pass
    elif msg.guild.get_role(poll_maker_id) in msg.author.roles and msg.channel.id == channel_id:
        try:
            if msg.content.split(" ")[0] == "!poll":
                pollinfo = msg.content.removeprefix('!poll').split('|')
                question = pollinfo[0]
                answerList = []
                emojiList = []
                await msg.delete()
                for entry in pollinfo[1:]:
                    entryList = entry.removeprefix(" ").removesuffix(" ").replace("  ", " ").split(' ')
                    if emoji.emojize(":" + entryList[0] + ":",use_aliases=True) != ":" + entryList[0] + ":":
                        emojiList.append(entryList[0])
                        answerList.append(" ".join(entryList[1:]))
                    else:
                        emojii = utils.get(msg.guild.emojis, name = entryList[0])
                        if emojii != None:
                                emojiList.append(emojii)
                                answerList.append(entryList[1])
                        else:
                            await (await msg.author.create_dm()).send(f"{entryList[0]} is not the name of an emoji. The poll will not be made.")
                            raise BreakIt
                text = question + "\n"
                for entry in emojiList:
                    try:
                        text += emoji.emojize(":" + entry + ":",use_aliases=True) + " - " + answerList[emojiList.index(entry)] + "\n"
                    except TypeError:
                        text += "<:" + entry.name + ":" + str(entry.id) + ">" + " - " + answerList[emojiList.index(entry)] + "\n"
                polmsg = await msg.channel.send(text)
                for entry in emojiList:
                    try:
                        await polmsg.add_reaction(emoji.emojize(":" + entry + ":",use_aliases=True))
                    except TypeError:
                        await polmsg.add_reaction(entry)
        except BreakIt:
                pass
    if msg.content.split(" ")[0] == "!helpme":
        embed=Embed(title="How do I use Polly?", description="Very simple :)! The command goes like this: `!pol <question> | <emoji name 1> <answer 1> | <emoji name 2> <answer 2> | ...` \nThe spaces before and after | are not needed. That's it! \nYou can delete a poll by adding a ❌ to a poll! :)", color=0xad3998)
        embed.set_author(name="Fesa", url="https://www.cubecraft.net/members/.224741/", icon_url=(await msg.guild.query_members(user_ids=[474319793042751491]))[0].avatar_url)
        embed.set_thumbnail(url=client.user.avatar_url)
        await msg.channel.send(embed=embed)


@client.event
async def on_reaction_add(rec, user):
    if user.guild.get_role(poll_maker_id) in user.roles and str(rec) == '❌' and rec.message.author == client.user:
        await rec.message.delete()
        
try:
    client.run(token)
except:
    print("Invalid token")