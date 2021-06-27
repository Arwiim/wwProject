"""Decorators
"""
import string
from random import choice
letters = string.ascii_lowercase + string.ascii_uppercase + '124567890'

def password_code():
    return ''.join([choice(letters) for x in range(12)])