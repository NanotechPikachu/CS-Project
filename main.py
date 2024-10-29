import discord
from discord.ext import commands
from jikanpy import Jikan
import mysql.connector as mys

jikan = Jikan()
con = mys.connect(host = 'localhost', user = 'root', passwd = '123', database = 'anime')
cur = None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix = '!!', 
    intents = intents
)

# FUNCTIONS
def anime_search(anime):
    data = jikan.search('anime', anime.lower())
    return data['data']
def addFav(anime, userId):
	q = f"INSERT INTO favorites VALUES ({userId}, '{anime}')"
	cur.execute(q)
	con.commit()
def createTable():
	q = 'CREATE TABLE IF NOT EXISTS favorites (userId BIGINT, anime CHAR(100))'
	cur.execute(q)
def getFav(userId):
	q = f'SELECT * FROM favorites WHERE userId={userId}'
	cur.execute(q)
	return cur.fetchall()
def checkFav(anime, userId):
	datas = getFav(userId)
	for data in datas:
		if data[1] == anime:
			return True
	return False

# CLASSES
class AnimeButtonView(discord.ui.View):
	def __init__(self, data):
		super().__init__()
		self.data = data
		self.datas = len(data) - 1
		self.c = 0
		self.embed = self.create_embed(self.c)

	def create_embed(self, index):
		embed = discord.Embed(
            title = self.data[index]['title'],
            url = self.data[index]['url'],
        )
		im = self.data[index]['images']['jpg']['image_url']
		titles = ''
		if self.data[index]['titles']:
			for i in self.data[index]['titles']:
				titles += f"{i['title']}, "
		desc = ''
		if self.data[index]['synopsis']:
			desc = self.data[index]['synopsis'][:1024]
		else:
			desc = 'N/A'
		last_dot = desc.rfind('.')
		if last_dot != -1:
			desc = desc[:1024 + 1]

		embed.add_field(
            name = 'Description',
            value = desc or 'N/A',
            inline = False
        )
		embed.add_field(
            name = 'Other Names',
            value = titles or 'N/A',
            inline = False
        )
		embed.add_field(
            name='Popularity',
            value=self.data[index]['popularity'] or 'N/A',
            inline=False
        )
		embed.add_field(
            name='Score',
            value=self.data[index]['score'] or 'N/A',
            inline=False
        )
		embed.set_image(url=im)
		return embed

	@discord.ui.button(label='Prev', style=discord.ButtonStyle.red)
	async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer()
		if self.c > 0:
			self.c -= 1
			self.embed = self.create_embed(self.c)
			self.children[1].disabled = False  # Next button
			if self.c == 0:
			
				self.children[0].disabled = True  # Prev button
				
			anime = self.embed.title
			author = interaction.user.id
			check = checkFav(anime, author)
			if check:
				self.children[2].disabled = True # Fav Button
			else:
				self.children[2].disabled = False # Fav Button
			await interaction.edit_original_response(embed=self.embed, view=self)

	@discord.ui.button(label='Next', style=discord.ButtonStyle.red)
	async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer()
		if self.c < self.datas - 1:
			self.c += 1
			self.embed = self.create_embed(self.c)
			self.children[0].disabled = False  # Prev button
			
			if self.c == self.datas:
				self.children[1].disabled = True  # Next button
			anime = self.embed.title
			author = interaction.user.id
			check = checkFav(anime, author)
			if check:
				self.children[2].disabled = True # Fav Button
			else:
				self.children[2].disabled = False # Fav Button
			await interaction.edit_original_response(embed = self.embed, view = self)

	@discord.ui.button(label='Favorite', style=discord.ButtonStyle.green)
	async def favorite(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.defer(ephemeral = True)
		anime = interaction.message.embeds[0].title
		author = interaction.user.id
		check = checkFav(anime, author)
		self.children[2].disabled = True # Fav Button
		addFav(anime, author)
		await interaction.edit_original_response(embed = self.embed, view = self)
		await interaction.followup.send('Added to favorite!', ephemeral = True)


@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}!')
	if con.is_connected():
		print('Connected to MySQL!')
		global cur
		cur = con.cursor()
		createTable()

@bot.command()
async def ping(ctx):
    await ctx.send('I am up!')

@bot.command()
async def anime(ctx, *anime):
	if not anime:
		return await ctx.send('No anime requested!')
	data = anime_search(' '.join(anime))

	if not data:
		return await ctx.send('Cannot find the requested anime!')
	
	view = AnimeButtonView(data)

	if checkFav(view.embed.title, ctx.author.id):
		view.children[2].disabled = True
	
	if view.c == 0:
		view.children[0].disabled = True  # Disable Prev button initially
	await ctx.send(embed = view.embed, view = view)

@bot.command(aliases = ['fav'])
async def favorites(ctx):
	fav = getFav(ctx.author.id)
	data = ''
	for i in fav:
		data += f'{i[1]}\n'
	embed = discord.Embed(
		title = 'Favorite Animes',
		description = data
	)
	await ctx.send(embed = embed)

bot.run('DISCORD BOT TOKEN')