import discord
import wavelink
import asyncio

from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def setup_hook(self):
        node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])
        wavelink.Player.autoplay = True

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.setup_hook())
        print('Music cog is ready.') 

    @commands.command()
    async def p(self, ctx, *, search):
        ''' Type !p. Play or add a song to queue. 
        Should be open music control table first.'''
        if not ctx.voice_client:
            await ctx.send(f'Let me join your voice channel first.')
            return
        vc: wavelink.Player = ctx.voice_client
        tracks = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            await ctx.send(f'No tracks found with query: `{search}`')
            return
        track = tracks[0]
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(track)
            await ctx.send(f'New queue was added. Now playing: {track.title}')
        else:
            vc.queue.put(track)
            await ctx.send(f'Added song {track.title} to queue.')

    @commands.command()
    async def join(self, ctx):
        ''' Let the bot join your voice channel. '''
        if not ctx.author.voice:
            await ctx.send(f'You are not connected to a voice channel')
            return
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            await ctx.send(f'I am already connected to your voice channel')

    @commands.command()
    async def leave(self, ctx):
        ''' Let the bot leave your voice channel. '''
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()

    async def disconnect(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        await ctx.send(f'Disconnecting...')
        await vc.disconnect()

    async def pause(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.is_paused():
            await ctx.send(f'Song has already been paused.')
            return
        else:
            await vc.pause()
            await ctx.send(f'Paused.')

    async def resume(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            await ctx.send(f'Song is playing.')
            return
        else:
            await vc.resume()   
            await ctx.send(f'Resumed.')

    async def skip(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.queue.is_empty:
            await ctx.send(f'Queue is empty. Disconnecting...')
            await vc.disconnect()
            return
        if vc.is_playing():
            await vc.stop()
            await ctx.send(f'Skipped.')
        else:
            await ctx.send(f'Nothing to skip.')
        
    async def queue(self, ctx):
        embed = discord.Embed(title='Playlist', color=discord.Color.blue())
        song_counter = 0
        vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            await ctx.send(f'Currently playing: {vc.current.title}')
        if vc.queue.is_empty:
            await ctx.send(f'Queue is empty.')
        else:
            queue = vc.queue.copy()
            for song in queue:
                song_counter += 1
                embed.add_field(name=f'[{song_counter}]. {song.title}', value=f'{song.title}', inline=False)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def mc(self, ctx):
        ''' Music control table. To acess, type !mc '''
        embed = discord.Embed(title='Music control table', 
                              description= 
                                f'To start playing music or add a song to queue, type !p <song name>.\n'
                                f'Notice: You and the bot must be in the same voice channel\n\n'
                                f'To pause the song, press ⏸️ button.\n\n'
                                f'To resume the song, press ▶️ button.\n\n'
                                f'To skip the song, press ⏭️ button.\n\n'
                                f'To see the queue, press 🗏 button.\n\n'
                                f'To disconnect the bot and exit music player, press ❌ button.\n\n',
                              color=discord.Color.magenta())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⏸️')
        await msg.add_reaction('▶️')
        await msg.add_reaction('⏭️')
        await msg.add_reaction('📄')
        await msg.add_reaction('❌')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⏸️', '▶️', '⏭️', '📄', '❌']
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=3600.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timed out.')
            return
        else:
            if str(reaction.emoji) == '⏸️':
                await self.pause(ctx)
                await self.mc(ctx)
            elif str(reaction.emoji) == '▶️':
                await self.resume(ctx)
                await self.mc(ctx)
            elif str(reaction.emoji) == '⏭️':
                await self.skip(ctx)
                await self.mc(ctx)
            elif str(reaction.emoji) == '📄':
                await self.queue(ctx)
                await self.mc(ctx)
            else:
                await self.disconnect(ctx)

                
async def setup(bot):
    await bot.add_cog(Music(bot))
