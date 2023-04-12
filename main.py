import openai
import discord
import os
from dotenv import load_dotenv

load_dotenv()

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.members = True  # Subscribe to the "members" intent

client = discord.Client(intents=intents)

messages = [{"role": "system", "content": "You are ChatGPT."}]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messages.append({"role":"user",
                     "content": message.content})


    async with message.channel.typing():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = messages
        )

        messages.append({"role":"assistant",
                        "content": response.choices[0]["message"].content})

    await message.channel.send(response.choices[0]["message"].content)

client.run(discord_bot_token)