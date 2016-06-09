import random

GREETINGS = [
    "Welcome to {}!",
    "Welcome!",
    "Can I help you?",
    "Welcome, can I help you?",
    "Welcome, what can I do to serve you?",
    "Hello, welcome to {}!",
    "Buy somethin' will ya!"
]


def get_merchant_greeting(location):
    greeting = str(random.choice(GREETINGS)).format(location.name)
    return '{} says "{}"'.format(location.npc.name, greeting)

#
# def get_merchant_greeting(location):
#     greeting = random.choice(GREETINGS)
#     return str(greeting).format(location.name)
#
