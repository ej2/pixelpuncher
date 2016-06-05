import random

GREETINGS = [
    "Welcome to {}!",
    "A warm welcome to you my friend.",
    "Greetings my friend.",
    "Salutations friend.",
    "Welcome to my humble store.",
    "Welcome!",
    "Welcome, what may I do to serve you?",
    "Greetings, what do you require?"
]


def get_merchant_greeting(location):
    greeting = random.choice(GREETINGS)
    return str(greeting).format(location.name)

