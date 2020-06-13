import discord, random, asyncio
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot

class Comics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def dateIsValid(self, date : str = None):
		# Checks if a passed date is a valid MM-DD-YYYY string
		if not date:
			# Auto to today's date
			date = dt.datetime.today().strftime("%m-%d-%Y")
		try:
			startDate = date.split("-")
		except ValueError:
			# Doesn't split by -?  Not valid
			return False
			
		if len(startDate) < 3:
			# Not enough values
			return False
			
		for d in startDate:
			try:
				int(d)
			except ValueError:
				return False
		
		return True
	def getRandDateBetween(self, first, last):
		# Takes two date strings "MM-DD-YYYY" and
		# returns a dict of day, month, and year values
		# from a random date between them
		fDate = first.split("-")
		fJDate = ComicHelper.date_to_jd(int(fDate[2]), int(fDate[0]), int(fDate[1]))
		lDate = last.split("-")
		lJDate = ComicHelper.date_to_jd(int(lDate[2]), int(lDate[0]), int(lDate[1]))
		
		# Get random Julian Date
		randJDate = random.uniform(fJDate, lJDate)
		
		# Convert to gregorian
		gDate = ComicHelper.jd_to_date(randJDate)
		yea   = int(gDate[0])
		mon   = int(gDate[1])
		day   = int(gDate[2])
		
		# Make sure all months/days are double digits
		if (int(mon) < 10):
			mon = "0"+str(mon)
		if (int(day) < 10):
			day = "0"+str(day)
		
		# Build our dict and return it
		newDate = { "Year" : str(yea), "Month" : str(mon), "Day" : str(day)}
		return newDate
	def isDateBetween(self, check, first, last):
		# Takes three date strings "MM-DD-YYY" and
		# returns whether the first is between the next two
		fDate = first.split("-")
		fJDate = ComicHelper.date_to_jd(int(fDate[2]), int(fDate[0]), int(fDate[1]))
		lDate = last.split("-")
		lJDate = ComicHelper.date_to_jd(int(lDate[2]), int(lDate[0]), int(lDate[1]))
		cDate = check.split("-")
		cJDate = ComicHelper.date_to_jd(int(cDate[2]), int(cDate[0]), int(cDate[1]))
		
		if cJDate <= lJDate and cJDate >= fJDate:
			return True
		else:
			return False
	@commands.command()
	async def randgmg(self, ctx):
		"""Randomly picks and displays a Garfield Minus Garfield comic."""
		
		channel = ctx.message.channel
		author  = ctx.message.author
		server  = ctx.message.guild
		
		
		# Can't be after this date.
		todayDate = dt.datetime.today().strftime("%m-%d-%Y")
		# Can't be before this date.
		firstDate = "02-13-2008"

		# Get a random Julian date between the first comic and today
		gotComic = False
		tries = 0
		while not gotComic:
		
			if tries >= 10:
				break
				
			date = getRandDateBetween(firstDate, todayDate)
			# Get URL
			getURL = "http://garfieldminusgarfield.net/day/" + date['Year'] + "/" + date['Month'] + "/" + date['Day']
			# Retrieve html and info
			imageHTML = await ComicHelper.getImageHTML(getURL)
		
			if imageHTML:
				imageURL  = ComicHelper.getGMGImageURL(imageHTML)
				if imageURL:
					gotComic = True
				
			tries += 1

		if tries >= 10:
			msg = 'Failed to find working link.'
			await ctx.send(msg)
			return
		
		imageDisplayName = "Garfield Minus Garfield Comic for " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
		# Download Image
		await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=ctx.author).send(ctx)
		# await GetImage.get(ctx, imageURL, imageDisplayName)
	@commands.command(pass_context=True)
	async def randpeanuts(self, ctx):
		"""Randomly picks and displays a Peanuts comic."""
		
		channel = ctx.message.channel
		author  = ctx.message.author
		server  = ctx.message.guild
	  
		# Can't be after this date.
		todayDate = dt.datetime.today().strftime("%m-%d-%Y")
		# Can't be before this date.
		firstDate = "10-02-1950"

		# Get a random Julian date between the first comic and today
		gotComic = False
		tries = 0
		while not gotComic:
		
			if tries >= 10:
				break
				
			date = getRandDateBetween(firstDate, todayDate)
			# Get URL
			getURL = "http://www.gocomics.com/peanuts/" + date['Year'] + "/" + date['Month'] + "/" + date['Day']
			# Retrieve html and info
			imageHTML = await ComicHelper.getImageHTML(getURL)
		
			if imageHTML:
				imageURL  = ComicHelper.getPeanutsImageURL(imageHTML)
				if imageURL:
					gotComic = True
				
			tries += 1

		if tries >= 10:
			msg = 'Failed to find working link.'
			await ctx.send(msg)
			return
		
		imageDisplayName = "Peanuts Comic for " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
		# Download Image
		await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=ctx.author).send(ctx)
		# await GetImage.get(ctx, imageURL, imageDisplayName)
	@commands.command(pass_context=True)
	async def randcalvin(self, ctx):
	    """Randomly picks and displays a Calvin & Hobbes comic."""
	    
	    channel = ctx.message.channel
	    author  = ctx.message.author
	    server  = ctx.message.guild
	    
	  
	    # Can't be after this date.
	    todayDate = "12-31-1995"
	    # Can't be before this date.
	    firstDate = "11-18-1985"

	    gotComic = False
	    tries = 0
	    while not gotComic:
	    
	        if tries >= 10:
	            break
	                    
	        date = getRandDateBetween(firstDate, todayDate)
	        # Get URL
	        # getURL = "http://marcel-oehler.marcellosendos.ch/comics/ch/" + date['Year'] + "/" + date['Month'] + "/" + date['Year'] + date['Month'] + date['Day'] + ".gif"
	        getURL = "http://downloads.esbasura.com/comics/Calvin%20and%20Hobbes/" + date["Year"] + "/" + "ch" + date["Year"][2:] + date["Month"] + date["Day"] + ".gif"

	        # Retrieve html and info
	        imageHTML = await ComicHelper.getImageHTML(getURL.strip(), "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
	    
	        if imageHTML:
	            imageURL  = getURL
	            gotComic = True
	            
	        tries += 1
	        
	    if tries >= 10:
	        msg = 'Failed to find working link.'
	        await channel.send(msg)
	        return
	        
	    imageDisplayName = "Calvin & Hobbes Comic for " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
	    # Download Image
	    await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=ctx.author).send(ctx)
	    # await GetImage.get(ctx, imageURL, imageDisplayName)
def setup(bot):
	bot.add_cog(Comics(bot))