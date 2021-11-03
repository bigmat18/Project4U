# --------------- GENERATION RANDOM SLUG STRING ----------------
import random
import string
from django.utils.text import slugify

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6

def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


def generate_slug(string):
    random_string = generate_random_string()
    if string is not None:
        slug = slugify(string)
        return str(slug + "-" + random_string)
    else: return str(random_string)
# --------------- GENERATION RANDOM SLUG STRING ----------------