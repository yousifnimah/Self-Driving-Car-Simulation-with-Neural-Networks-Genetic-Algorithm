import itertools
import os
import pyglet.image as image
from pyglet.graphics import Batch
from pyglet.shapes import Circle
from pyglet.text import Label
import json


class Track:
    def __init__(self, index):
        self.track_image = image.load(os.path.join("images_", f"track{index}.png"))
        self.track_overlay = image.load(os.path.join("images_", f"track{index}-overlay.png"))
        self.background_batch = Batch()
        #car checkpoint
        with open(os.path.join("images_", f"track{index}.json"), "r") as file:
            data = json.load(file)

        self.checkpoints = data["checkpoints"]

        self.checkpoint_spirits = []
        for index, checkpoint in enumerate(self.checkpoints):
            self.checkpoint_spirits.append((
                Circle(checkpoint[0], checkpoint[1], 20, color=(250, 250, 250, 120), batch=self.background_batch),
                Label(str(index), checkpoint[0], checkpoint[1], anchor_x="center", anchor_y="center", batch=self.background_batch),
            ))

        pitch = self.track_image.width * len("RGBA")
        pixels = self.track_image.get_image_data().get_data("RGBA", pitch)

        map = [1 if b in [(54, 54, 54, 255), (53, 117, 12, 255),(55, 119, 12, 255),(54, 118, 11, 255), (75, 75 ,75,255), (63, 131, 12, 255)]  else 0 for b in itertools.batched(pixels, 4)]
        self.map_matrix = [map[n: n + self.track_image.width] for n in range(0, self.track_image.width * self.track_image.height, self.track_image.width)]

    def is_road(self, x, y):
        if (x < 0 or x >= self.track_image.width) or (y < 0 or y >= self.track_image.height):
            return False
        return self.map_matrix[int(y)][int(x)] == 1