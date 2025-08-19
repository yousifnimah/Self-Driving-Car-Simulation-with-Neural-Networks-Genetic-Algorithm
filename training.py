from canvas import Canvas
from network import Network
from evolution import Evolution
from storage import Storage
import os

car_image_paths = [os.path.join("images_", f"car{i}.png") for i in range(6)]

storage = Storage("brain.json")

network_dimensions = 5,4,2
population_count = 10
max_simulation_rounds = 400
keep_count = 4

canvas = Canvas(2, car_image_paths)

networks = [Network(network_dimensions) for _ in range(population_count)]
evolution = Evolution(population_count, keep_count)

best_chromosomes = storage.load()
for c,n in zip(best_chromosomes, networks):
    n.deserialize(c)

simulation_round = 1
while simulation_round <= max_simulation_rounds and canvas.is_simulation:
    print("simulation round: ", simulation_round)
    canvas.generate_simulation(networks, simulation_round)
    simulation_round += 1
    if canvas.is_simulation:
        print(f"--- average check points of the network --- {sum(n.highest_checkpoint for n in networks) / len(networks):.2f}.")
        serialized = [network.serialize() for network in networks]
        offspring = evolution.execute(serialized)
        storage.save(offspring[:keep_count])

        # create network from offspring
        networks = []
        for chromosome in offspring:
            network = Network(network_dimensions)
            network.deserialize(chromosome)
            networks.append(network)

