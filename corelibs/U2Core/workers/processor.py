from actor import Actor
from port import Port

# Producer
producer_actor = Actor("Producer")
producer_actor.add_output(Port("output", False))

# Processor
upper_actor = Actor("UpperCase")
upper_actor.add_input(Port("input", True))
upper_actor.add_output(Port("output", False))

# Consumer
consumer_actor = Actor("Consumer")
consumer_actor.add_input(Port("input", True))


producer = InputWorker(producer_actor)

processor = UpperCaseWorker(upper_actor)

consumer = OutputWorker(consumer_actor)


from communication_channel import CommunicationChannel

# Producer -> UpperCase
channel1 = CommunicationChannel()

producer.buses["output"].add_channel(channel1)
processor.buses["input"].add_channel(channel1)

# UpperCase -> Consumer
channel2 = CommunicationChannel()

processor.buses["output"].add_channel(channel2)
consumer.buses["input"].add_channel(channel2)


producer.tick()
processor.tick()
consumer.tick()