from flask import Flask, request

bot = Flask(__name__)


@bot.route('/')
def handle():

    print("bruh")
    return "hey"
