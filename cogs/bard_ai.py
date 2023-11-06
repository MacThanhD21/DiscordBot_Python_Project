from discord.ext import commands
import os
from bardapi import Bard
from dotenv import load_dotenv


load_dotenv()
BARDAPI_KEY = os.getenv('BARDAPI_KEY')
bard = Bard(token=BARDAPI_KEY)
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


class BardAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ask(self, ctx, *, question):
        ''' Ask BARD AI a question '''
        try:
            user_name = ctx.author.display_name

            await ctx.send(f'```BardBot reply {user_name} :```')

            response = bard.get_answer(question)
            content = response.get('content', '')
            image_List = response.get('images', list())
            # print(response)
            # print(*lines)
            # print(*image_urls)
            lines = content.split('\n')
            
            j = 0
            for i in range(max(len(lines), len(image_List))):
                if lines[i].strip() and j < len(image_List) and "[Image" in lines[i]:
                    await ctx.send(image_List[j])
                    j += 1
                if lines[i].strip() and not lines[i].startswith("[Image"):
                    await ctx.send(lines[i])
        except Exception as e:
            error_message = (
                f"**Error 😣:**\n\n"
                f"```\n"
                f"{str(e)}\n"
                f"```\n"
            )
            await ctx.send(error_message)


async def setup(bot):
    await bot.add_cog(BardAI(bot))
