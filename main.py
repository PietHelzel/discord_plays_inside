import discord
from dotenv import load_dotenv
from discord.ext import commands

from input_handler import InputHandler, InputKey, EventKind

# -----------------------------------------------------------------------------------------------------------------------
# discord connection

load_dotenv()
intents = discord.Intents().all()
client = commands.Bot(command_prefix = '!', intents = intents)

input_handler = InputHandler()
input_handler.run()

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    if channel == "discord-plays-inside": # channel name here
        print(f'{username}: {user_message}')

    if message.author != client.user:
        process_input(user_message)

def process_input(message):

    message_parts = message.split(" ")

    try:
        command = message_parts[0].lower()
        time_value = float(message_parts[1])

        if time_value < 26 and time_value > 0:
            match command:
                case "right": input_handler.register_keypress(0, time_value, InputKey.RIGHT)
                case "left":  input_handler.register_keypress(0, time_value, InputKey.LEFT)
                case "up":    input_handler.register_keypress(0, time_value, InputKey.UP)
                case "down":  input_handler.register_keypress(0, time_value, InputKey.DOWN)


    except (ValueError, IndexError):
        match message.lower():
            case "jump":
                input_handler.register_keypress(0, 0.1, InputKey.UP)
            case "jump right":
                input_handler.register_keypress(0, 0.2, InputKey.RIGHT)
                input_handler.register_keypress(0.1, 0.1, InputKey.UP)
            case "jump left":
                input_handler.register_keypress(0, 0.2, InputKey.LEFT)
                input_handler.register_keypress(0.1, 0.1, InputKey.UP)
            case "use":
                input_handler.register_keypress(0, 0.3, InputKey.GRAB)
            case "hold":
                input_handler.register_event(0, InputKey.GRAB, EventKind.PRESS)
            case "release":
                input_handler.register_event(0, InputKey.GRAB, EventKind.RELEASE)
            case "enter":
                input_handler.register_keypress(0, 0.2, InputKey.ENTER)
            case "stop":
                input_handler.stop_all()


client.run('') # token here
