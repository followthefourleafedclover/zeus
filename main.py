from discord.ext import commands
import discord 
import os
from dotenv import load_dotenv
import logging
from Paginators import Paginator, StatefulPaginator
from UI import UIComponent

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s   %(message)s',  
    handlers=[ 
        logging.StreamHandler()  
    ]
)

intents = discord.Intents.default() 
intents.messages = True
intents.message_content = True 

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='/', intents=intents) 


@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        logging.info(f"Command tree synced: {len(synced)} commands available.")
    except Exception as e:
        logging.errors(f"Error syncing command tree: {e}")

data = [f"Item {i}" for i in range(1, 101)] 
@bot.command()
async def basic(ctx):
    paginator = Paginator(
        items=data,
        items_per_page=10)
    await paginator.start(ctx)  


@bot.command()
async def button(ctx):
    ui_component = UIComponent()

    button1 = ui_component.create_button("Click Me!", "button_1")
    button2 = ui_component.create_button("Next Page", "button_next", discord.ButtonStyle.secondary)

    view = ui_component.create_view(button1, button2)

    await ctx.send("Choose an option:", view=view)

@bot.command()
async def state(ctx): 
    paginator = StatefulPaginator(
        items=data,
        items_per_page=10
    )
    await paginator.start(ctx)




if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables.")
    else:
        bot.run(TOKEN)