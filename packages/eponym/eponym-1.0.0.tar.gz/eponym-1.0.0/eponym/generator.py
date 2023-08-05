from eponym.data.descriptors import DESCRIPTORS
from eponym.data.things import THINGS
import random


def generate_username():
    username = str()
    username += random.choice(DESCRIPTORS)
    username += random.choice(DESCRIPTORS)
    username += random.choice(THINGS)
    username += str(random.randint(0, 9))
    username += str(random.randint(0, 9))
    username += str(random.randint(0, 9))
    username += str(random.randint(0, 9))
    return username
