import random
import math


class Layer:
    def __init__(self, inputs_count, outputs_count):
        self.outputs = [0.0 for _ in range(outputs_count)]
        self.weights = [[random.random() * 2 - 1 for _ in range(inputs_count)] for _ in range(outputs_count)]

    def feed_forward(self, inputs):
        for output_index, output in enumerate(self.outputs):
            sum_ = 0
            for weight_index, inpt in enumerate(inputs):
                sum_ += inpt * self.weights[output_index][weight_index]
            self.outputs[output_index] = math.tanh(sum_) # to keep results between -1.0 - 1.0

class Network:
    def __init__(self, dimensions): # [5,3,2]
        self.layers = []
        self.inputs = []
        self.dimensions = dimensions
        self.highest_checkpoint = 0
        for n in range(len(dimensions) - 1):
            self.layers.append(Layer(dimensions[n], dimensions[n + 1]))

    def feed_forward(self, inputs):
        self.inputs = inputs
        for layer in self.layers:
            layer.feed_forward(inputs)
            inputs = [i for i in layer.outputs]
        return self.layers[-1].outputs

    def serialize(self):
        chromosome = []
        for layer in self.layers:
            for output in layer.weights:
                for weight in output:
                    chromosome.append(weight)

        return RankableChromosome(self.highest_checkpoint, chromosome)

    def deserialize(self, chromosome):
        layer_index = 0
        output_index = 0
        input_index = 0
        for gene in chromosome:
            self.layers[layer_index].weights[output_index][input_index] = gene
            input_index += 1
            if input_index > len(self.layers[layer_index].weights[output_index]) - 1:
                input_index = 0
                output_index += 1
                if output_index > len(self.layers[layer_index].weights) - 1:
                    output_index = 0
                    layer_index += 1

class RankableChromosome:
    def __init__(self, highest_checkpoint, chromosome):
        self.highest_checkpoint = highest_checkpoint
        self.chromosome = chromosome

    def __lt__(self, other):
        return self.highest_checkpoint > other.highest_checkpoint
