import random
import string


def generate_random_string():
    def string_generator(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    words = []

    for _ in range(100):
        word = string_generator(random.randint(3, 8))
        word = word + "-" + string_generator(random.randint(3, 8)) + "-" + str(random.randint(1, 999)).zfill(3)
        words.append(word)

    return words
