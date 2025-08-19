from pyglet.shapes import Circle
from pyglet.text import Label

class NeuronSprite:
    def __init__(self, x,y ,batch):
        self.node_border = Circle(x,y, 18, color=(0,0,0,120), batch=batch)
        self.node_fill = Circle(x,y, 17, color=(255,255,255,120), batch=batch)
        self.node_value = Label(x=x, y=y, font_size=8, batch=batch, anchor_x="center", anchor_y="center")

    def update(self, value):
        self.node_value.text = f"{value:.2f}"
        if value > 0:
            self.node_fill.color = 0, int(value * 200), 0, 120
        else:
            self.node_fill.color = int(value * 200),0, 0, 120

class Hud:
    def __init__(self, dimensions, simulation_rounds, batch):
        self.neurons = []
        self.simulation_round = simulation_rounds
        self.simulation_rounds_label = Label(f"Generation: {simulation_rounds}", x=15, y=510,font_size=13, batch=batch)
        self.speed_label = Label(x=150, y=510, font_size=13, batch=batch)
        self.populations_alive_label = Label(x=250, y=510, font_size=13, batch=batch)

        x = 50
        for neuron_count in dimensions:
            height = neuron_count * 50 - 10
            y = 540 - (540 - height) / 2
            for _ in range(neuron_count):
                self.neurons.append(NeuronSprite(x,y,batch))
                y -= 50
            x += 50


    def update(self, network, simulation_rounds,speed, population_total, population_alive):
        self.speed_label.text = f"Speed: {int(speed)}"
        self.simulation_rounds_label.text = f"Generation: {simulation_rounds}"
        self.populations_alive_label.text = f"Population: {population_alive}/{population_total}"

        input_index = 0
        for input_value in network.inputs:
            self.neurons[input_index].update(input_value)
            input_index += 1

        for layer in network.layers:
            for value in layer.outputs:
                self.neurons[input_index].update(value)
                input_index += 1

