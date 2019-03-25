FROM python:3.5
ADD bot.py /
RUN pip install discord.py
RUN pip install requests
CMD [ "python", "./bot.py" ]