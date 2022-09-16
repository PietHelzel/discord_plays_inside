import discord
from dotenv import load_dotenv
from discord.ext import commands
import pydirectinput

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

# -----------------------------------------------------------------------------------------------------------------------      

def process_input(message):

    message_parts = message.split(" ")

    try:
        command = message_parts[0].lower()
        time_value = float(message_parts[1])

        if time_value < 11 and time_value > 0:
            match command:
                case "w": input_handler.register_keypress(0, time_value, InputKey.W)
                case "a": input_handler.register_keypress(0, time_value, InputKey.A)
                case "s": input_handler.register_keypress(0, time_value, InputKey.S)
                case "d": input_handler.register_keypress(0, time_value, InputKey.D)
                case "run":
                    input_handler.register_keypress(0, time_value, InputKey.SHIFT)
                    input_handler.register_keypress(0, time_value, InputKey.W)


        if time_value < 361 and time_value > 0:
            pixels = int(time_value*(1520/360))
            match command:
                case "right": pydirectinput.move(pixels, None)
                case "left":  pydirectinput.move(-pixels, None)
                case "up":    pydirectinput.move(None, -pixels)
                case "down":  pydirectinput.move(None, pixels)



    except (ValueError, IndexError):
        match message.lower():
            case "jump":
                input_handler.register_keypress(0, 0.2, InputKey.SPACE)

            case "jump w":
                input_handler.register_keypress(0, 0.7, InputKey.W)
                input_handler.register_keypress(0.1, 0.2, InputKey.SPACE)

            case "use":
                input_handler.register_keypress(0, 5, InputKey.E)

            case "call":
                input_handler.register_keypress(0, 0.1, InputKey.Q)

            case "sneak":
                input_handler.register_keypress(0, 0.1, InputKey.CTRL)
                input_handler.register_keypress(5.1, 0.1, InputKey.CTRL)

            case "tab":
                input_handler.register_keypress(0, 0.1, InputKey.TAB)

            case "1":
                input_handler.register_keypress(0, 0.1, InputKey.ONE)

            case "2":
                input_handler.register_keypress(0, 0.1, InputKey.TWO)

            case "3":
                input_handler.register_keypress(0, 0.1, InputKey.THREE)

            case "tab":
                pydirectinput.click

            case "stop":
                input_handler.stop_all()

# -----------------------------------------------------------------------------------------------------------------------      

client.run('') # token here
