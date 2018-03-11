

class Character(object):
    name = ""
    player = None
    location = None

    def __init__(self, name, player, location):
        self.name = name
        self.player = player
        self.location = location

    def __str__(self):
        return self.name

    def get_player(self):
        return self.player

    def get_location(self):
        return self.location

    # This function does NOT check whether the room to be moved to is a
    # valid target, that should be checked prior to this call
    def move_character(self, new_location):
        self.location.remove_character(self)
        new_location.add_character(self)
        self.location = new_location

