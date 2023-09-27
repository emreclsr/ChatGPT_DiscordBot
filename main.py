import openai
import discord
import os
from dotenv import load_dotenv
from loguru import logger
from textwrap import wrap

load_dotenv()

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
organizationID = os.getenv("ORGANIZATION_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

logger.debug("Environment loaded.")

intents = discord.Intents.default()
intents.members = True  # Subscribe to the "members" intent

client = discord.Client(intents=intents)

logger.debug("Discord client set.")

messages = [{"role": "system", "content": "You are ChatGPT"}]


@client.event
async def on_message(message):
    if message.author == client.user:
        logger.debug(f"Message from {message.author}")
        return

    messages.append({"role": "user",
                     "content": message.content})

    logger.debug("Message sending to ChatGPT.")

    async with message.channel.typing():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            organization=organizationID
        )

        logger.debug(f"ChatGPT send the response")

        response_message = response.choices[0]["message"].content

        messages.append({"role": "assistant",
                        "content": response_message})

        logger.debug("Message wrapped for sending part by part.")
        send_messages = wrap(response_message, 1000)

        logger.debug(f"Message sending.")
        for mes in send_messages:
            await message.channel.send(mes)

client.run(discord_bot_token)