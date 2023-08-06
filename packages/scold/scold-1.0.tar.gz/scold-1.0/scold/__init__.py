import string
from .words import Words


def scold(template="You are ${adjective}!"):
    if template == None:
        template = "None"
    template = string.Template(template)
    result = template.substitute(Words())
    return result
