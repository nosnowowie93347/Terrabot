@echo off
echo Starting setup of Terrabot...
echo installing dependencies, this could take a bit...
pip install -r requirements.txt
pause
echo Now you must add the bot's token.
pause
notepad .env
echo now edit the config file.
pause
notepad utils/config.py
echo After adding the token and setting up the config file, the setup is complete!