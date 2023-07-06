import validators
from urllib.parse import urlparse


def cutting_url(address):
    if validators.url(address) and len(address) <= 255:
        x = urlparse(address)
        cutted_url = (f"{x.scheme}://{x.hostname}")
        return cutted_url
