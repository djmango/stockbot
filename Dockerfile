FROM python:3.5
ADD bot.py /
ADD cogs /cogs
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./bot.py"]