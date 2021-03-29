import discord
from discord.ext import commands
import asyncio
import requests
from PIL import Image
import PIL
import cv2 as cv
from io import BytesIO
import io
import random
import numpy as np

class Images(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name='fry',aliases=['deepfry'])
	async def fry(self, ctx: commands.Context,help="",amount="20"):
		img,amount,successful = await self.getImage(ctx,"fry",help,amount)
		if not successful:
			if(amount==0): #Error command
				em = discord.Embed()
				em.title = f'Error when running command'
				em.description = f"Error: {img}."
				em.color = 0xEE0000
				await ctx.send(embed=em)
				return
			else: #Help Command
				em = discord.Embed()
				em.title = f'Usage: /fry [img|imgURL] [gamma]'
				em.description = f'Deep-fries the image attached, url in the message, or the image attached before the command. Change gamma based on how dark the image is. Default gamma value is 20, range 1-500. Saturation default 3, range: 1-50'
				em.add_field(name="Aliases", value="/deepfry", inline=False)
				em.add_field(name="Examples", value="/fry https://imgur.com/a/wUChw7w | /deepfry (imageAttachment)", inline=False)
				em.color = 0x22BBFF
				await ctx.send(embed=em)
				return
		await ctx.send("Processing... (This may take a while)")
		toDelete = await self.getMessages(ctx,1)
		# Processing
		img = np.array(img) #convert PIL image to Numpy (CV2 works with numpy BRG arrays)
		# Convert RGB to BGR 
		img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
		width, height = img.shape[:2]
		#Increase brightness
		value = int(amount)*6 #default multiplier, change depending on dark/light images
		hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
		h, s, v = cv.split(hsv)
		lim = 255 - value
		v[v > lim] = 255
		v[v <= lim] += value
		final_hsv = cv.merge((h, s, v))
		img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
		#Sharpen
		kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) #how to modify a pixel based on surrounding pixels
		img = cv.filter2D(img, -1, kernel)
		#Change gamma and make it crusty
		gamma = int(amount)
		table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
		img = cv.LUT(img, table)
		#Now deform the image a bit
		from skimage.transform import swirl #import works here but if at the beginning, breaks the code for some reason
		#swirl the image at random places
		for x in range(8):
			img = swirl(img, strength=((random.random()+1)*-1**x), radius=width/1.4,center=(random.randint(int(width/4),int(width-width/4)),random.randint(int(height/4),int(height-height/4))))
			img = (img*255).astype('uint8')
		#convert CV2 Numpy array to PIL
		img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #Change CV2 BGR to RGB
		im_pil = Image.fromarray(img)   #Convert to PIL
		# Increase saturation
		from PIL import ImageEnhance
		from PIL import ImageFilter
		converter = PIL.ImageEnhance.Color(im_pil)
		im_pil = converter.enhance(0.4)
		im_pil = im_pil.filter(ImageFilter.EDGE_ENHANCE_MORE) #add edge detection
		# Convert to an attachable Discord Format
		arr = io.BytesIO() #convert to bytes array
		im_pil.save(arr, format='PNG')
		arr.seek(0) #seek back to beginning of file
		# Send
		await ctx.send(file=discord.File(arr,'fry.png'))
		await ctx.channel.delete_messages(toDelete)

	@commands.command(name='radial',aliases=['radialblur','blur','funny'])
	async def radial(self, ctx: commands.Context,help="",amount="10"):
		img,amount,successful = await self.getImage(ctx,"radial",help,amount)
		if not successful:
			if(amount==0): #Error command
				em = discord.Embed()
				em.title = f'Error when running command'
				em.description = f"Error: {img}."
				em.color = 0xEE0000
				await ctx.send(embed=em)
				return
			else: #Help Command
				em = discord.Embed()
				em.title = f'Usage: /radial [img|imgURL] [amount]'
				em.description = f'Adds radial blur to the image attached, url in the message, or the image attached before the command by [amount] from 1 to 50'
				em.add_field(name="Aliases", value="/blur /radialblur /funny", inline=False)
				em.add_field(name="Examples", value="/radialblur https://imgur.com/a/wUChw7w | /blur (imageAttachment) 30", inline=False)
				em.color = 0x22BBFF
				await ctx.send(embed=em)
				return()
		await ctx.send("Processing... (This may take a while)")
		toDelete = await self.getMessages(ctx,1)
		# Processing
		img = np.array(img) #convert PIL image to Numpy (CV2 works with numpy BRG arrays)
		# Convert RGB to BGR 
		img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
		w, h = img.shape[:2]
		# Radial Blur
		center_x = w / 2
		center_y = h / 2
		blur = amount/1000
		iterations = 5
		growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
		shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
		growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
		shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)

		for i in range(iterations):
			tmp1 = cv.remap(img, growMapx, growMapy, cv.INTER_LINEAR)
			tmp2 = cv.remap(img, shrinkMapx, shrinkMapy, cv.INTER_LINEAR)
			img = cv.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)

		#convert CV2 Numpy array to PIL
		img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #Change CV2 BGR to RGB
		im_pil = Image.fromarray(img)   #Convert to PIL
		# Convert to an attachable Discord Format
		arr = io.BytesIO() #convert to bytes array
		im_pil.save(arr, format='PNG')
		arr.seek(0) #seek back to beginning of file
		# Send
		await ctx.send(file=discord.File(arr,'radial.png'))
		await ctx.channel.delete_messages(toDelete)

	@commands.command(name='swirl')
	async def swirl(self, ctx: commands.Context,help="",amount="10"):
		img,amount,successful = await self.getImage(ctx,"radial",help,amount)
		if not successful:
			if(amount==0): #Error command
				em = discord.Embed()
				em.title = f'Error when running command'
				em.description = f"Error: {img}."
				em.color = 0xEE0000
				await ctx.send(embed=em)
				return
			else: #Help Command
				em = discord.Embed()
				em.title = f'Usage: /swirl [img|imgURL] [amount]'
				em.description = f'Swirls the image attached, url in the message, or the image attached before the command by [amount] from -100 to 100'
				em.add_field(name="Examples", value="/swirl https://imgur.com/a/wUChw7w | /swirl (imageAttachment) 30", inline=False)
				em.color = 0x22BBFF
				await ctx.send(embed=em)
				return()
		await ctx.send("Processing... (This may take a while)")
		toDelete = await self.getMessages(ctx,1)
		# Processing
		from skimage.transform import swirl #import works here but not at the beginning
		w,h = img.size
		img = np.array(img) #convert PIl image to Numpy
		# Swirl
		img = swirl(img, strength=amount, radius=w/1.3)
		img = (img*255).astype('uint8')
		#convert numpy array to Pillow img
		im_pil=Image.fromarray(img)
		# Convert to an attachable Discord Format
		arr = io.BytesIO() #convert to bytes array
		im_pil.save(arr, format='PNG')
		arr.seek(0) #seek back to beginning of file
		# Send
		await ctx.send(file=discord.File(arr,'swirl.png'))
		await ctx.channel.delete_messages(toDelete)

	@commands.command(name='warp')
	async def warp(self, ctx: commands.Context,help="",amount="0"):
		img,amount,successful = await self.getImage(ctx,"warp",help,amount)
		if not successful:
			if(amount==0): #Error command
				em = discord.Embed()
				em.title = f'Error when running command'
				em.description = f"Error: {img}."
				em.color = 0xEE0000
				await ctx.send(embed=em)
				return
			else: #Help Command
				em = discord.Embed()
				em.title = f'Usage: /warp [img|imgURL]'
				em.description = f'Randomly warps the image attached, url in the message, or the image attached before the command'
				em.add_field(name="Examples", value="/warp https://imgur.com/a/wUChw7w | /warp (imageAttachment)", inline=False)
				em.color = 0x22BBFF
				await ctx.send(embed=em)
				return()
		await ctx.send("Processing... (This may take a while)")
		toDelete = await self.getMessages(ctx,1)
		# Processing
		from skimage.transform import swirl #import works here but not at the beginning
		img = np.array(img) #convert PIl image to Numpy
		# Swirl
		width, height = img.shape[:2]
		for x in range(5):
			img = swirl(img, strength=((random.random()+1)*-1**x), radius=width/1.4,center=(random.randint(int(width/4),int(width-width/4)),random.randint(int(height/4),int(height-height/4))))
			img = (img*255).astype('uint8')
		#convert numpy array to Pillow img
		im_pil=Image.fromarray(img)
		# Convert to an attachable Discord Format
		arr = io.BytesIO() #convert to bytes array
		im_pil.save(arr, format='PNG')
		arr.seek(0) #seek back to beginning of file
		# Send
		await ctx.send(file=discord.File(arr,'warp.png'))
		await ctx.channel.delete_messages(toDelete)

	async def getImage(self, ctx: commands.Context,command="",help="",amount="30",amount2="1"):
		if(help=="help"):
			return(("",1,False)) #help command
		if(help!=""): #if given url or number
			if(self.validateURL(help)): #check if given url
				url = help
				response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}) #use safari user agent in case they are blocking python UA
				img = Image.open(BytesIO(response.content))
				if(self.validateNum(amount,command)):
					amount = int(amount)
					return((img,amount,True))
				else:
					return("Invalid Number. Make sure the number is in a valid range. Type 'help' after the command to check the range",0,False)
			else: 
				if(self.validateNum(help,command)): #check if given number
					amount = help
					help = ""
				else:
					return("Invalid URL/Number. The 1st parameter you gave was invalid. Check if the link has an image or if the number is in a valid range",0,False)
		if(help==""):
			try: #get image from attachment
				url = ctx.message.attachments[0].url
				response = requests.get(url)
				img = Image.open(BytesIO(response.content))
				return((img,int(amount),True))
			except IndexError: #get image above if no image attached
				imgCache = await self.getMessages(ctx,2)
				for x in range(1,len(imgCache)):
					try:
						url = imgCache[x].attachments[0].url
						response = requests.get(url)
						img = Image.open(BytesIO(response.content))
						return((img,int(amount),True))
					except IndexError:
						continue
				return(("No image found. Did you mean to show the help menu? Type 'help' after the command to show (without quotation marks)",0,False))



	def validateURL(self, url):
		try:
			if not requests.get(url).status_code == 200:
				return False
			image_formats = ("image/png", "image/jpeg", "image/jpg")
			h = requests.head(url, timeout=1)
			if not (h.headers["content-type"] in image_formats):
				return(False)
			return True
		except requests.exceptions.MissingSchema:
			return False

	def validateNum(self, num,command):
		if(command=="radial"):
			min,max = -100,100
		elif(command=="blur"):
			min,max = 1,50
		elif(command=="fry"):
			min,max = 1,500
		else:
			min,max = -1000,1000
		try:
			return(int(num)>=min and int(num)<=max)
		except ValueError:
			return(False)

	async def getMessages(self,ctx: commands.Context,number: int=1):
		if(number==0):
			return([])
		toDelete = []
		async for x in ctx.channel.history(limit = number):
			toDelete.append(x)
		return(toDelete)

	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		em = discord.Embed()
		em.title = f'Error: {__name__}'
		em.description = f"{error}"
		em.color = 0xEE0000
		await ctx.send(embed=em)
def setup(bot):
	bot.add_cog(Images(bot))