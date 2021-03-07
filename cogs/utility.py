import discord
import asyncio
from discord.ext import commands
import bot_info
import pymongo
import media_cache
import string
import database as db

class Utility(commands.Cog):
    def __init__(self, bot):
        '''
        mongo_url = bot_info.data['mongo_url']
        self.mongo_client = pymongo.MongoClient(mongo_url)
        mongo_url = ''

        self.db = self.mongo_client['gman']
        self.inv = self.db['inventory']'''

        self.valid_label_chars = string.ascii_letters + string.digits + ' '
        self.bot = bot

    @commands.command()
    async def undo(self, ctx):
        # Limiting to 2 so that you don't undo/delete the last video gman can use
        vid_msg_id = list(db.vids.find({'channel':str(ctx.channel.id)}).sort('_id', - 1).limit(2))
        #await ctx.send(vid_msg_id)
        if(len(vid_msg_id) <= 1):
            await ctx.send("Out of undos!")
            return
        vid_msg_id = vid_msg_id[0]['message_id']
        
        vid_to_undo = await ctx.fetch_message(int(vid_msg_id))
        await vid_to_undo.delete()
        await ctx.message.delete()
        db.vids.delete_one({'message_id': vid_msg_id})
    

    # ======== BOOKMARKS/INVENTORY SYSTEM ========

    def cleanup_label(self, label):
        return ''.join(c for c in label.strip() if c in self.valid_label_chars)

    @commands.command()
    async def save(self, ctx, *, label : str = ''):
        dirty_label = label.strip()
        label = self.cleanup_label(dirty_label)
        
        video = media_cache.get_from_cache(str(ctx.channel.id))
        if(video is None):
            await ctx.send("There is no video to bookmark, upload one and try again")
            return
        video = video[-1]

        query = {'user':ctx.author.id, 'label':label}
        new_values = {'$set': {'video':video}}
        result = db.inv.update_one(query, new_values, upsert=True)
        if(dirty_label != label): # Needed to remove some invalid chars from label
            await ctx.send(f'I saved your bookmark as `{label}`')
        else: # Label was clean from the start!
            await ctx.message.add_reaction('\U0001F44D')
    @commands.command()
    async def store(self, ctx, *, label : str = ''):
        await self.save(ctx, label)
    


    @commands.command()
    async def load(self, ctx, *, label : str = ''):
        label = self.cleanup_label(label)
        
        result = db.inv.find_one({'user':ctx.author.id, 'label':label})
        if(result is None):
            await ctx.message.add_reaction('\u274C')
        else:
            await ctx.send(result['video'])
    @commands.command()
    async def use(self, ctx, *, label : str = ''):
        await self.load(ctx, label)


    
    @commands.command()
    async def delete(self, ctx, label : str = ''):
        label = self.cleanup_label(label)
        result = db.inv.delete_one({'user':ctx.author.id, 'label':label})
        if(result is not None and result.deleted_count == 1):
            await ctx.message.add_reaction('\U0001F44D')
        else:
            await ctx.message.add_reaction('\u274C')
    @commands.command()
    async def remove(self, ctx, label : str = ''):
        await self.delete(ctx, label)



    @commands.command()
    async def bookmarks(self, ctx):
        bookmark_list = []
        for bookmark in db.inv.find({'user':ctx.author.id}):
            label = bookmark['label']
            if(label != ''):
                bookmark_list.append(f'* {label}')
        if(len(bookmark_list) > 0):
            msg = 'Here are your bookmarks! Load one by doing `!load <bookmark_name>`:\n```'
            msg += '\n'.join(bookmark_list)
            msg += '```'
            await ctx.send(msg)
        else:
            await ctx.send("You don't have any bookmarks, you can add one with `!save <bookmark_name>`")


        
        



def setup(bot):
    bot.add_cog(Utility(bot))
