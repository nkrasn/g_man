import asyncio
import bot_info
import database as db
import discord
from discord.ext import commands
import media_cache
import os
import re
import sys
import traceback


# If any videos were not deleted while the bot was last up, remove them
vid_files = [f for f in os.listdir('vids') if os.path.isfile(os.path.join('vids', f))]
for f in vid_files:
    os.remove(f'vids/{f}')


extensions = ['cogs.bitrate', 'cogs.filter', 'cogs.fun', 'cogs.corruption', 'cogs.bookmarks', 'cogs.utility']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), help_command=None)

# Loads extensions, returns string saying what reloaded
def reload_extensions(exs):
    module_msg = ''
    for ex in exs:
        try:
            bot.unload_extension(ex)
            bot.load_extension(ex)
            module_msg += 'module "{}" reloaded\n'.format(ex)
        except Exception as e:
            module_msg += 'reloading "{}" failed, error is:```{}```\n'.format(ex, e)
    return module_msg

    
    
    
    
# Set up stuff
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="!help"))
    global extensions
    print(reload_extensions(extensions))

# Process commands
@bot.event
async def on_message(message):
    # Adding URLs to the cache
    if(len(message.attachments) > 0):
        msg_url = message.attachments[0].url
        if(not msg_url.endswith('_ignore.mp4') and msg_url.split('.')[-1] in media_cache.approved_filetypes):
            media_cache.add_to_cache(message, message.attachments[0].url)
            print("Added file!")
    elif(re.match(media_cache.discord_cdn_regex, message.content)):
        media_cache.add_to_cache(message, message.content)
        print("Added discord cdn url!")
    elif(re.match(media_cache.yt_regex, message.content) or re.match(media_cache.twitter_regex, message.content) or re.match(media_cache.tumblr_regex, message.content)):
        media_cache.add_to_cache(message, message.content)
        print("Added yt/twitter/tumblr url! " + message.content)

    await bot.process_commands(message)

# Forgetting videos that get deleted
@bot.event
async def on_message_delete(message):
    db.vids.delete_one({'message_id':str(message.id)})

# Command error
@bot.event
async def on_command_error(ctx, error):
    if(not isinstance(error, commands.CommandNotFound)):
        await ctx.send('Oops, something is wrong!\n```\n' + repr(error) + '\n```')
        #print(error)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
# Reloading extensions
@bot.command(description='Reloads extensions. Usage: /reload [extension_list]', pass_context=True)
@bot_info.is_owner()
async def reload(ctx, *, exs : str = None):
    module_msg = 'd' # d
    if(exs is None):
        module_msg = reload_extensions(extensions)
    else:
        module_msg = reload_extensions(exs.split())
    await ctx.send(module_msg)

for ex in extensions:
    try:
        bot.load_extension(ex)
    except Exception as e:
        print('Failed to load {} because: {}'.format(ex, e))


# Start the bot
bot.run(bot_info.data['login'])
