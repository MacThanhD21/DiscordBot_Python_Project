import discord
import asyncio
import random

choice = ['🪨', '📄', '✂️']

async def rps(ctx, bot):
    check = True
    while check:
        msg = await ctx.send(embed=discord.Embed(
            title='Rock-paper-scissors!',
            description='Choose your weapon!\nTo exit, click ❌.'))
        await msg.add_reaction('🪨')
        await msg.add_reaction('📄')
        await msg.add_reaction('✂️')
        await msg.add_reaction('❌')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['🪨', '📄', '✂️', '❌']
        reaction, user = await bot.wait_for('reaction_add', timeout=100.0, check=check)
        if str(reaction.emoji) == '❌':
            await ctx.send('Game ended.')
            check = False
            break
        bot_choice = random.choice(choice)
        win = {'🪨': '✂️', '📄': '🪨', '✂️': '📄'}
        lose = {'🪨': '📄', '📄': '✂️', '✂️': '🪨'}
        tie = {'🪨': '🪨', '📄': '📄', '✂️': '✂️'}
        if (str(reaction.emoji), bot_choice) in lose.items():
            await ctx.send(f'You lose! {bot_choice} beats {str(reaction.emoji)}.')
        elif (str(reaction.emoji), bot_choice) in win.items():
            await ctx.send(f'You win! {str(reaction.emoji)} beats {bot_choice}.')
        else:
            await ctx.send(f'It\'s a tie! {str(reaction.emoji)} ties with {bot_choice}.')
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=2)
    return
