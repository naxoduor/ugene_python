class Actor:

    def __init__(self, name):

        self.name = name

        self.input_ports = []

        self.output_ports = []

    def add_input(self, port):
        self.input_ports.append(port)

    def add_output(self, port):
        self.output_ports.append(port)

    def get_ports(self):
        return self.input_ports + self.output_ports