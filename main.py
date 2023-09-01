import discord
import asyncio

from elevenlabs import generate, save
from elevenlabs import set_api_key

from key import elevenlabs_key
from key import discord_token
from gpt import comp


set_api_key(elevenlabs_key)
voice_model = "Adam"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def generate_and_send_audio(channel, generated_response):
    print("Initializing Audio Generation\n")
    audio = generate(text=generated_response, voice=voice_model, model='eleven_multilingual_v1')
    save(audio, "Asis.mp3")
    await channel.send(file=discord.File("Asis.mp3"))
    print("Audio Generated, Asis is Free for New Requests\n")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Ei Asis"))

@client.event
async def on_message(message):
    if message.content.lower().startswith('ei asis'):
        print('User Requested GPT-3 Auto Completion')
        user_input = message.content.lower().split('ei asis',)[1]
        if user_input:
            generated_response = comp(user_input)
            await message.channel.send(generated_response)
            print("GPT-3 Auto Completion Done\n")

            asyncio.create_task(generate_and_send_audio(message.channel, generated_response))
        else:
            await message.channel.send("<@{user}> como posso ajudar?".format(user=message.author.id))

client.run(discord_token)
