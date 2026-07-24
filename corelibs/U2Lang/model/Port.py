class Port:

    def __init__(self, name, is_input):

        self.name = name

        self.is_input = is_input

        self.peer = None

    def set_peer(self, peer):
        self.peer = peer

    def get_peer(self):
        return self.peer