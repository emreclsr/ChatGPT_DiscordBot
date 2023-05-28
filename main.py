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

messages = [{"role": "system", "content": "You are ChatGPT"}]

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

        # await message.channel.send(response_message)

        split_response = response_message.split("\n\n")
        send_messages = []
        plain_text_message = ""
        code_text_message = ""
        for m in split_response:
            # Check is a code message
            if m[:3] == "```":
                # Send previous plain text message
                if plain_text_message != "":
                    send_messages.append(plain_text_message)
                    plain_text_message = ""
                #
                code_text_message += f"{m}\n\n"
            # If code message continues
            elif code_text_message != "":
                code_text_message += f"{m}\n\n"
                # If code message finished
                if m[-3:] == "```":
                    send_messages.append(code_text_message)
                    code_text_message = ""
            else:
                plain_text_message += f"{m}\n\n"
                # Divide message every 1000 characters because od discord message lenght
                if len(plain_text_message) > 1000:
                    send_messages.append(plain_text_message)
                    plain_text_message = ""

        logger.debug(f"Message sending.")
        for m in send_messages:
            await message.channel.send(m)

    if len(messages) > 10:
        del messages[2]
        del messages[3]


client.run(discord_bot_token)