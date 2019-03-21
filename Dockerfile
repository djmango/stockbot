FROM python:3
ADD bot.py /
RUN pip install --user -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
CMD [ "python", "./bot.py" ]