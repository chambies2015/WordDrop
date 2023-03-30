import os
import random
import discord
from discord.ext import commands, tasks
from discord import Embed
import creds
from discord import File

token = creds.bot_token

accepted_channels = ['1090828602397970472']


def read_five_letter_words(filename):
    with open(filename, "r") as file:
        words = [line.strip() for line in file]
    return words


filename = "five_letter_words.txt"
five_letter_words = read_five_letter_words(filename)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

word_of_the_day = random.choice(five_letter_words)


@bot.event
async def on_ready():
    change_word.start()
    print(f"{bot.user} has connected to Discord!")


@tasks.loop(hours=24)
async def change_word():
    global word_of_the_day
    word_of_the_day = random.choice(five_letter_words)


@bot.command(name="guess", help="Used to guess the 5-letter word.")
async def guess(ctx, *, user_word):
    if ctx.channel.id != 1090828602397970472:
        return
    user_word = user_word.lower()
    response = ""

    wotd = word_of_the_day

    if len(user_word) != 5:
        response = "Please enter a 5-letter word."
    elif user_word == word_of_the_day:
        embed = Embed(title=f"🎉Congratulations! You guessed the word: {word_of_the_day} 🎉")
        await ctx.send(embed=embed)
        change_word.restart()
        return
    else:
        correct_chars = [c1 if c1 == c2 else "_" for c1, c2 in zip(user_word, word_of_the_day)]
        response = f"Your guess: {user_word}\nCorrect characters: {' '.join(correct_chars)}"
        response = f"```\n{response}\n```"

    await ctx.send(response)


@bot.command(name="listwords", help="Show all possible 5-letter words.")
async def list_words(ctx):
    if ctx.channel.id != accepted_channels:
        return
    file_to_upload = File("five_letter_words.txt", filename="five_letter_words.txt")
    await ctx.send("All possible words:", file=file_to_upload)


@bot.command(name="nebulahelp")
async def help(ctx):
    if ctx.channel.id != accepted_channels:
        return
    await ctx.send("Commands for")


bot.run(token)
