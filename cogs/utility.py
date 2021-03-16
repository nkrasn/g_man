import discord
import asyncio
from discord.ext import commands
import video_creator
import database as db

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    async def _gif(self, ctx, vstream, astream, kwargs):
        return (vstream, astream, {})
    @commands.command()
    async def gif(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._gif, {'is_gif':True})

    
    async def _mp3(self, ctx, vstream, astream, kwargs):
        return (vstream, astream, {})
    @commands.command()
    async def mp3(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._mp3, {'is_mp3':True})
    

    @commands.command()
    async def swap(self, ctx):
        channel_id = str(ctx.channel.id)
        vids = list(db.vids.find({'channel':channel_id}).sort('_id', -1).limit(2))
        if(len(vids) < 2):
            await ctx.send("I don't see two videos to swap.")
            return
        new_vid, old_vid = vids

        await ctx.send(old_vid['url'])
        old_vid_msg = await ctx.fetch_message(int(old_vid['message_id']))
        
    
    async def _timestamp(self, ctx, vstream, astream, kwargs):
        vstream = (
            vstream
            .filter('fps', fps=100)
            .filter('scale', w=480, h=-2)
            .drawtext(
                text="%{pts}",
                #x="main_w/2 - tw/2", y="main_h/2 - th/2",
                x="15", y="main_h - th*2 - 35",
                fontsize=40, fontcolor="white", borderw=2, bordercolor="black",
                escape_text=False
            )
        )
        return vstream, astream, {}
    @commands.command()
    async def timestamp(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._timestamp, {})
    @commands.command()
    async def time(self, ctx):
        await self.timestamp(ctx)

    
    @commands.command()
    async def undo(self, ctx):
        # Limiting to 2 so that you don't undo/delete the last video gman can use
        vid_msg_id = list(db.vids.find({'channel':str(ctx.channel.id)}).sort('_id', -1).limit(2))
        #await ctx.send(vid_msg_id)
        if(len(vid_msg_id) <= 1):
            await ctx.send("Out of undos!")
            return
        vid_msg_id = vid_msg_id[0]['message_id']
        
        vid_to_undo = await ctx.fetch_message(int(vid_msg_id))
        await vid_to_undo.delete()
        await ctx.message.delete()
        db.vids.delete_one({'message_id': vid_msg_id})



        



def setup(bot):
    bot.add_cog(Utility(bot))
