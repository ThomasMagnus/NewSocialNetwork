from random import choice
import random


def generate_random_num():
    random_num = ''
    random_list = list('123456789')
    for i in range(random.randint(3, 9)):
        random_num += choice(random_list)

    return random_num
