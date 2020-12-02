import json
import discord
from discord.ext import commands

# Load bot info (contains login and owners)
data = None
with open('bot_info.json') as f:
    data = json.load(f)

# Returns true if you can use dev commands (like reload)
def is_owner():
    def predicate(ctx):
        return str(ctx.message.author.id) in data['owners']
    return commands.check(predicate)
