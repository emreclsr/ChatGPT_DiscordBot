import openai
import discord
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

logger.debug("Environment loaded.")

intents = discord.Intents.default()
intents.members = True  # Subscribe to the "members" intent

client = discord.Client(intents=intents)

logger.debug("Discord client set.")

messages = [{"role": "system", "content": "You are ChatGPT."}]

@client.event
async def on_message(message):
    if message.author == client.user:
        logger.debug(f"Message from {message.author}, message: {message}")
        return

    logger.debug(f"New message from {message.author}, message: {message}")

    messages.append({"role":"user",
                     "content": message.content})

    logger.debug("Message sending to ChatGPT.")

    async with message.channel.typing():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = messages
        )

        logger.debug(f"ChatGPT send the response: {response}")

        response_message = response.choices[0]["message"].content

        messages.append({"role":"assistant",
                        "content": response_message})

        logger.debug(f"Check response longer than 2000 characters: {len(response_message)}")

        send_messages = []
        i=0
        if len(response_message) > 2000:
            while i<len(response_message):
                logger.debug(f"Message longer than 2000 characters spliting.")
                send_messages.append(response_message[i:i+2000])
                # send_messages.append(" ")
                i += 2000
        else:
            logger.debug(f"Message not longer than 2000 characters.")
            send_messages.append(response_message)

        logger.debug(f"Message sending.")
        for m in send_messages:
            await message.channel.send(m)

client.run(discord_bot_token)