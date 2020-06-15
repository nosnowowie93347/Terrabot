import asyncio, discord, base64, binascii, re, math, shutil, tempfile, os
from   discord.ext import commands
from discord.ext.commands import Bot
from   Cogs import Nullify, DL
class Encode(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	# Check hex value
	def _check_hex(self, hex_string):
		# Remove 0x/0X
		hex_string = hex_string.replace("0x", "").replace("0X", "")
		hex_string = re.sub(r'[^0-9A-Fa-f]+', '', hex_string)
		return hex_string

	# To base64 methods
	def _ascii_to_base64(self, ascii_string):
		ascii_bytes = self._to_bytes(ascii_string)
		base_64     = base64.b64encode(ascii_bytes)
		return self._to_string(base_64)

	def _hex_to_base64(self, hex_string):
		hex_string    = self._check_hex(hex_string)
		hex_s_bytes   = self._to_bytes(hex_string)
		hex_bytes     = binascii.unhexlify(hex_s_bytes)
		base64_bytes  = base64.b64encode(hex_bytes)
		return self._to_string(base64_bytes)

	# To ascii methods
	def _hex_to_ascii(self, hex_string):
		hex_string  = self._check_hex(hex_string)
		hex_bytes   = self._to_bytes(hex_string)
		ascii_bytes = binascii.unhexlify(hex_bytes)
		return self._to_string(ascii_bytes)

	def _base64_to_ascii(self, base64_string):
		base64_bytes  = self._to_bytes(base64_string)
		ascii_bytes   = base64.b64decode(base64_bytes)
		return self._to_string(ascii_bytes)

	# To hex methods
	def _ascii_to_hex(self, ascii_string):
		ascii_bytes = self._to_bytes(ascii_string)
		hex_bytes   = binascii.hexlify(ascii_bytes)
		return self._to_string(hex_bytes)

	def _base64_to_hex(self, base64_string):
		b64_string = self._to_bytes(base64_string)
		base64_bytes = base64.b64decode(b64_string)
		hex_bytes    = binascii.hexlify(base64_bytes)
		return self._to_string(hex_bytes)

	def _rgb_to_hex(self, r, g, b):
		return '#%02x%02x%02x' % (r, g, b)

	def _hex_to_rgb(self, _hex):
		_hex = _hex.replace("#", "")
		l_hex = len(_hex)
		return tuple(int(_hex[i:i + l_hex // 3], 16) for i in range(0, l_hex, l_hex // 3))

	def _cmyk_to_rgb(self, c, m, y, k):
		c, m, y, k = [float(x)/100.0 for x in tuple([c, m, y, k])]
		return tuple([round(255.0 - ((min(1.0, x * (1.0 - k) + k)) * 255.0)) for x in tuple([c, m, y])])

	def _rgb_to_cmyk(self, r, g, b):
		c, m, y = [1 - x/255 for x in tuple([r, g, b])]
		min_cmy = min(c, m, y)
		return tuple([0,0,0,100]) if all(x == 0 for x in [r, g, b]) else tuple([round(x*100) for x in [(x - min_cmy) / (1 - min_cmy) for x in tuple([c, m, y])] + [min_cmy]])
	@commands.command()
	async def color(self, ctx, *, value = None):
		"""
		View info on a rgb, hex or cmyk color and their
		values in other formats

		Example usage:
		color #3399cc
		color rgb(3, 4, 5)
		"""
		if not value:
			await ctx.send("Usage: `{}color [value]`".format(ctx.prefix))
			return

		value = value.lower()
		
		if not any(value.startswith(x) for x in ["#", "rgb", "cmyk"]):
			await ctx.send("Invalid value color format, please choose from rgb, cmyk or hex")
			return

		error = False

		if value.startswith('rgb'):
			count = value.count('(') + value.count(')') + value.count(',')
			if count != 4:
				error = True

			number_list = value.lower().replace("rgb", "").replace("(", "").replace(")", "").replace(" ", "")
			try:
				r, g, b = map(int, number_list.split(','))

				if (r < 0 or r > 255) or (g < 0 or g > 255) or (b < 0 or b > 255):
					error = True

			except:
				error = True

			if error:
				await ctx.send("Invalid RGB color format!")
				return
			
			_hex = self._rgb_to_hex(r,g,b)
			c, m, y, k = self._rgb_to_cmyk(r, g, b)
			
			embed_color = int("0x{}".format(_hex.replace("#", '')), 16)
			embed = discord.Embed(color=embed_color)

			embed.title = "Color {}".format(value.replace(" ", ""))
			embed.add_field(name="Hex", value=_hex)
			embed.add_field(name="CMYK", value="cmyk({}, {}, {}, {})".format(c, m, y, k))
				
		elif value.startswith('#'):
			match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
			if not match:
				await ctx.send("Invalid Hex color format!")
				return

			embed_color = int("0x{}".format(value.replace('#', '')), 16)
			embed = discord.Embed(color=embed_color)
			r, g, b = self._hex_to_rgb(value)
			c, m, y, k = self._rgb_to_cmyk(r, g, b)

			embed.title = "Color {}".format(value.replace(" ", ""))
			embed.add_field(name="RGB", value="rgb({}, {}, {})".format(r, g, b))
			embed.add_field(name="CMYK", value="cmyk({}, {}, {}, {})".format(c, m, y, k))

		elif value.startswith('cmyk'):
			count = value.count('(') + value.count(')') + value.count(',')
			if count != 5:
				error = True

			number_list = value.lower().replace("cmyk", "").replace("(", "").replace(")", "").replace(" ", "")

			try:
				c, m, y, k = map(int, number_list.split(','))

				if (c < 0 or c > 255) or (m < 0 or m > 255) or (y < 0 or y > 255) or (k < 0 or k > 255):
					error = True

			except:
				error = True
			
			if error:
				await ctx.send("Invalid CMYK color format!")
				return
	
			r, g, b = self._cmyk_to_rgb(c, m, y, k)
			_hex = self._rgb_to_hex(r, g, b)

			embed_color = int("0x{}".format(_hex.replace("#", '')), 16)
			embed = discord.Embed(color=embed_color)

			embed.title = "Color {}".format(value.replace(" ", ""))
			embed.add_field(name="Hex", value=_hex)
			embed.add_field(name="RGB", value="rgb({}, {}, {})".format(r, g, b))
		await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(Encode(bot))