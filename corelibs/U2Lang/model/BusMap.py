class BusMap:

    def __init__(self, mapping=None):
        self.mapping = mapping or {}

    def compose(self, message):

        new_data = {}

        for key, value in message.data.items():

            mapped = self.mapping.get(key, key)

            new_data[mapped] = value

        return new_data

    def reduce(self, message):

        new_data = {}

        reverse = {v: k for k, v in self.mapping.items()}

        for key, value in message.data.items():

            mapped = reverse.get(key, key)

            new_data[mapped] = value

        return new_data