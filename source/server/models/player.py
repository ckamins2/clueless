
class Player(object):
    name = ""
    character = None

    def __init__(self, name, character):
        self.name = name
        self.character = character

    def __init__(self, name):
        self.name = name

    def set_character(self, character):
        self.character = character