from .pagintor import Paginator
import discord 
import asyncio

#<Stateful Paginator - Can be used to store user data and persit over mutiple command interaction> 
class StatefulPaginator(Paginator): 
    def __init__(self, *args, state_store={}, **kwargs): 
        super().__init__(*args, **kwargs)
        self.state_store = state_store 

    def get_state(self, user_id):
        return self.state_store.get(user_id, 0) 

    def set_state(self, user_id, page):
        self.state_store[user_id] = page

    async def start(self, ctx):
        self.current_page = self.get_state(ctx.author.id) 
        self.message = await ctx.send(embed=self.create_embed(), view=self.create_view(ctx))
        if self.timeout: 
            await asyncio.sleep(self.timeout)
            await self.message.edit(view=None)

    def create_view(self, ctx):
        view = super().create_view(ctx)
        
        async def first_button_callback(interaction: discord.Interaction):
            self.set_state(interaction.user.id, 0) 
            self.current_page = self.get_state(interaction.user.id)
            await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        async def prev_button_callback(interaction: discord.Interaction):
            if self.current_page > 0:
                self.current_page -= 1
                self.set_state(interaction.user.id, self.current_page)
                await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        async def next_button_callback(interaction: discord.Interaction):
            if self.current_page < self.get_total_pages() - 1:
                self.current_page += 1
                self.set_state(interaction.user.id, self.current_page)
                await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        async def last_button_callback(interaction: discord.Interaction):
            self.current_page = self.get_total_pages() - 1
            self.set_state(interaction.user.id, self.current_page)
            await interaction.response.edit_message(embed=self.create_embed(), view=self.create_view(ctx))

        view.children[0].callback = first_button_callback
        view.children[1].callback = prev_button_callback
        view.children[2].callback = next_button_callback
        view.children[3].callback = last_button_callback
        
        return view 