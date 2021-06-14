import asyncio
import discord
from discord.ext import commands
import database as db
import ffmpeg
import filter_helper
import media_cache
import re
import video_creator

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    async def _download(self, ctx, vstream, astream, kwargs):
        return vstream, astream, {}
    @commands.command()
    async def download(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._download, {})
    @commands.command()
    async def fix(self, ctx):
        await self.download(ctx)
    

    async def _gif(self, ctx, vstream, astream, kwargs):
        fps = kwargs['fps']
        vstream = vstream.filter('fps', fps=fps).split()
        palette = vstream[1].filter('palettegen')
        vstream = ffmpeg.filter([vstream[0], palette], 'paletteuse')
        return vstream, astream, {}
    @commands.command()
    async def gif(self, ctx, fps : int = 24):
        fps = max(1, min(fps, 24))
        await video_creator.apply_filters_and_send(ctx, self._gif, {'is_gif':True, 'fps':fps})


    @commands.command()
    async def help(self, ctx, command_name : str = ''):
        if(command_name == ''):
            await ctx.send('https://github.com/nkrasn/g_man/blob/master/COMMANDS.md')
            return
        if(command_name == 'filter'):
            await ctx.send('For more information about the filter command, please read: https://github.com/nkrasn/g_man/blob/master/COMMANDS.md#filter-command')
            return
        if(command_name == 'help'):
            await ctx.send('`!help` to get a list of all the commands.\n`!help <command_name>` to get help on a specific command.')
            return

        commands_file = open('COMMANDS.md', 'r')
        all_commands = commands_file.read().split('\n')
        commands_file.close()

        embed = None
        for command in all_commands:
            if(command == '' or command[0] != '|' or command.startswith('| Command') or command.startswith('| ---')):
                continue
            command = re.split(r'^\| | \| |\| | \|$', command)
            if(command[0] == ''):
                command = command[1:]
            if(command[-1] == ''):
                command = command[:-1]
            command = {
                'names' : command[0].split('<br>'),
                'syntax' : command[1].replace('<br><br>','\n'),
                'limits' : command[2].replace('<br>', '\n'),
                'description' : command[3].replace('<br>', '\n').replace('\|', '|'),
                'examples' : command[4].replace('<br><br>', '\n').replace('\|', '|')
            }

            if(command_name not in command['names']):
                continue
            embed = discord.Embed(title=command_name, description=command['description'])
            embed.add_field(name='Syntax', value=command['syntax'], inline=False)
            if(command['limits'] != ''):
                embed.add_field(name='Min/Max Values', value=command['limits'], inline=False)
            if(command['syntax'] != command['examples']):
                embed.add_field(name='Examples', value=command['examples'], inline=False)
            if(len(command['names']) > 1):
                aliases = list(filter(lambda x : x != command_name, command['names']))
                aliases = ', '.join(aliases)
                embed.set_footer(text=f'NOTE: this command is also known as:\n{aliases}')

            await ctx.send(embed=embed)
            break

        if(embed is None):
            await ctx.send("Command not found, here's a list of all the commands: https://github.com/nkrasn/g_man/blob/master/COMMANDS.md")


    @commands.command()
    async def link(self, ctx):
        vid_link = media_cache.get_from_cache(str(ctx.message.channel.id))[0]
        await ctx.send(f'`{vid_link}`')


    
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
        speed_change = kwargs['speed_change']
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
        if(speed_change != 1.0):
            vstream, astream = filter_helper.apply_speed(vstream, astream, speed_change)
        return vstream, astream, {}
    @commands.command()
    async def timestamp(self, ctx, speed_change : float = 1.0):
        await video_creator.apply_filters_and_send(ctx, self._timestamp, {'is_ignored_mp4':True, 'speed_change':speed_change})
    @commands.command()
    async def time(self, ctx, speed_change : float = 1.0):
        await self.timestamp(ctx, speed_change)

    
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
