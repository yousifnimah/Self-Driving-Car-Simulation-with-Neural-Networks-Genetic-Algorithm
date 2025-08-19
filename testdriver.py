from canvas import Canvas
from network import Network
from evolution import Evolution
from storage import Storage
import os

car_image_paths = [os.path.join("images_", f"car{i}.png") for i in range(6)]
storage = Storage("brain.json")

network_dimensions = 5,4,2
population_count = 3
max_simulation_rounds = 5
keep_count = 4

canvas = Canvas(2, car_image_paths)

networks = [Network(network_dimensions) for _ in range(population_count)]

best_chromosomes = storage.load()
for c,n in zip(best_chromosomes, networks):
    n.deserialize(c)

simulation_round = 1
while simulation_round <= max_simulation_rounds and canvas.is_simulation:
    canvas.generate_simulation(networks, simulation_round)
    simulation_round += 1

