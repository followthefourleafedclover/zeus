import discord 
from discord.ui import *
import __main__ as main 
import asyncio

# <Parent Class Paginator> 
class Paginator:
    def __init__(self, items : list, items_per_page : int, generate_page=None, timeout=None, button_labels=None, embed_customization=None, show_all_buttons=True):
        self.items = items
        self.items_per_page = items_per_page
        self.generate_page = generate_page if generate_page else lambda page_data: discord.Embed(description="\n".join(page_data))
        self.timeout = timeout
        self.current_page = 0
        self.button_labels = button_labels if button_labels else {
            'previous': '⬅️ Previous',
            'next': 'Next ➡️',
            'first': '⏪ First',
            'last': 'Last ⏩'
        }

        self.embed_customization = embed_customization if embed_customization else {
            'title': 'Paginator',
            'color': discord.Color.blue(),
            'footer': 'Page Navigation',
        }

        self.show_all_buttons = show_all_buttons

    def get_total_pages(self):
        return -(-len(self.items) // self.items_per_page) 

    def get_page_items(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return self.items[start:end]

    def create_embed(self):
        page_data = self.get_page_items()
        embed = self.generate_page(page_data)

        embed.title = self.embed_customization.get('title', 'Paginator')
        embed.color = self.embed_customization.get('color', discord.Color.blue())
        embed.set_footer(text=self.embed_customization.get('footer', 'Page Navigation'))

        embed.set_footer(text=f"Page {self.current_page + 1}/{self.get_total_pages()}")
        return embed

    async def start(self, ctx):
        self.message = await ctx.send(embed=self.create_embed(), view=self.create_view(ctx))
        if self.timeout: 
            await asyncio.sleep(self.timeout)
            await self.message.edit(view=None)

    def create_view(self, ctx):
        view = View()
        
        first_button = Button(label=self.button_labels['first'], style=discord.ButtonStyle.primary, custom_id="first")
        prev_button = Button(label=self.button_labels['previous'], style=discord.ButtonStyle.primary, custom_id="prev")
        next_button = Button(label=self.button_labels['next'], style=discord.ButtonStyle.primary, custom_id="next")
        last_button = Button(label=self.button_labels['last'], style=discord.ButtonStyle.primary, custom_id="last")

        async def first_button_callback(interaction: discord.Interaction):
            if self.current_page != 0:
                self.current_page = 0
                await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        async def prev_button_callback(interaction: discord.Interaction):
            if self.current_page > 0:
                self.current_page -= 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        async def next_button_callback(interaction: discord.Interaction):
            if self.current_page < self.get_total_pages() - 1:
                self.current_page += 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        async def last_button_callback(interaction: discord.Interaction):
            if self.current_page != self.get_total_pages() - 1:
                self.current_page = self.get_total_pages() - 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        first_button.callback = first_button_callback
        prev_button.callback = prev_button_callback
        next_button.callback = next_button_callback
        last_button.callback = last_button_callback

        if self.show_all_buttons:
            view.add_item(first_button)
            view.add_item(prev_button)
            view.add_item(next_button)
            view.add_item(last_button)
        else:
            view.add_item(prev_button)
            view.add_item(next_button)

        if self.current_page == 0:
            prev_button.disabled = True
            first_button.disabled = True
        if self.current_page == self.get_total_pages() - 1:
            next_button.disabled = True
            last_button.disabled = True

        return view
    
