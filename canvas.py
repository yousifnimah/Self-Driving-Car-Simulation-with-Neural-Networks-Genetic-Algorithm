import random
import time

from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.window import Window, key
from pyglet import image
from hud import Hud
from car import Car
from track import Track
from math import sqrt


class Canvas(Window):
    frame_duration = 1/60
    car_sprites = []

    def __init__(self, track_index, car_image_paths):
        super().__init__()


        self.title = "Simulator"
        self.is_simulation = True
        self.width = 960
        self.height = 540
        self.total_population = 0
        self.population_alive = 0
        self.simulation_rounds = 0

        # hud
        self.overlay_batch = Batch()
        self.hud = None

        #background
        self.background_batch = Batch()
        # track part
        self.track = Track(track_index)


        self.background_sprite = Sprite(self.track.track_image, batch=self.background_batch)
        self.track_overlay = Sprite(self.track.track_overlay, batch=self.overlay_batch)

        #car part
        self.cars_batch = Batch()
        self.radar_batch = Batch()
        self.cars_images = [image.load(c) for c in car_image_paths]

    def generate_simulation(self, networks ,simulation_rounds):
        self.hud = Hud(networks[0].dimensions,self.simulation_rounds, batch=self.overlay_batch)

        self.simulation_rounds = simulation_rounds
        last_update = time.perf_counter()
        for network in networks:
            self.car_sprites.append(Car(network, self.track ,random.choice(self.cars_images), self.cars_batch, self.radar_batch))

        self.total_population = len(self.car_sprites)
        self.population_alive = self.total_population

        while self.is_simulation and self.population_alive > 0:
            elapsed_time = time.perf_counter() - last_update
            if elapsed_time > self.frame_duration:
                last_update = time.perf_counter() # update last time with recent performance time
                self.dispatch_events() # register all events
                self.update(elapsed_time)
                self.draw()

        for car in self.car_sprites:
            car.network.highest_checkpoint = car.last_checkpoint_passed

        self.car_sprites.clear()

    def update(self, delta_time):
        for car in self.car_sprites:
            car.update(delta_time)
            self.check_checkpoint(car)
            if not self.track.is_road(car.body.x, car.body.y):
                car.shutdown_engine()

        running_cars = [c for c in self.car_sprites if c.is_running]
        self.population_alive = len(running_cars)

        if self.population_alive > 0:
            self.hud.update(running_cars[0].network,self.simulation_rounds,self.car_sprites[0].speed, self.total_population, self.population_alive)

    def draw(self):
        self.clear()
        self.background_batch.draw()
        self.track.background_batch.draw()
        self.radar_batch.draw()
        self.cars_batch.draw()
        self.overlay_batch.draw()
        self.flip()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.is_simulation = False
            print("Simulation ended")

    def check_checkpoint(self, car_sprite):
        for index, checkpoint in enumerate(self.track.checkpoints):
            distance = sqrt((car_sprite.body.x - checkpoint[0]) ** 2 + (car_sprite.body.y - checkpoint[1]) ** 2)
            if distance < 40:
                car_sprite.hit_checkpoint(index)
