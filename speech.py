# Speech to Discord for BlazeBot (cog)

import discord
from discord.ext import commands
from discord.ext.commands import Bot

# Import Speech Recognition Library
import speech_recognition as sr

# Import Windows 10 TTS Library
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

# Message displayed when command is run (It will only say this message out loud on Windows 10)
startup_mesg = "What would you like to post to Discord?"


class Speech(commands.Cog):
		def __init__(self, bot):
				self.bot = bot

		@commands.command(pass_context=True)
		async def speech(self, ctx):
				"""Post to Discord via voice"""
				r = sr.Recognizer()
				with sr.Microphone() as source:
							# Print and say startup message
							print(startup_mesg)
							speak.Speak(startup_mesg)
							# Listen to microphone
							audio = r.listen(source)

							# Store the voice input in a variable
							recognised = r.recognize_google(audio)

							output = "Now posting your message to Discord: " + recognised
							print(output)
							speak.Speak(output)
							await ctx.send(recognised)
		@commands.command(pass_context=True)
		async def speechtts(self, ctx):
				"""Post to Discord via voice (TTS)"""
				r = sr.Recognizer()
				with sr.Microphone() as source:
							# Print and say startup message
							print(startup_mesg)
							speak.Speak(startup_mesg)
							# Listen to microphone
							audio = r.listen(source)

				# Store the voice input in a variable
				recognised = r.recognize_google(audio)

				output = "Now posting your message to Discord with TTS enabled: " + recognised
				print(output)
				speak.Speak(output)
				await ctx.send(recognised, tts=True)
def setup(client):
		client.add_cog(Speech(client))
