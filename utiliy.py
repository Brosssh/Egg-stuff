import hashlib
from itertools import chain, repeat

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def ask_and_wait_valid_answer(list_possible,question):
    prompts = chain([question], repeat("Not valid, please try again: "))
    replies = map(input, prompts)
    valid_response = next(filter(list_possible.__contains__, replies))
    return valid_response

def ask_and_wait_pos_integer(question):
    prompts = chain([question], repeat("Not valid, please try again: "))
    replies = map(input, prompts)
    numeric_strings = filter(str.isnumeric, replies)
    numbers = map(int, numeric_strings)
    is_positive = (0.).__lt__
    valid_response = next(filter(is_positive, numbers))
    return valid_response
