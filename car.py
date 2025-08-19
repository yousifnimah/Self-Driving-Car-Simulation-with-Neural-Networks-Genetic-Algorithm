import math
from pyglet.sprite import Sprite
from pyglet.shapes import Line

class Radar:
    max_length_pixels = 200
    def __init__(self, angle, batch):
        self.angle = angle
        self.beam = Line(0,0,0,0, 1.5, color=(255,255,255,100), batch=batch)


class Car:
    max_speed = 6
    slipping_speed = max_speed * 0.75
    def __init__(self, network, track ,image, batch, radar_batch):
        image.anchor_x = 30
        image.anchor_y = 30
        self.track = track
        self.body = Sprite(image, batch=batch)
        self.body.x, self.body.y = self.track.checkpoints[0][0], self.track.checkpoints[0][1]
        self.speed = 0.0
        self.rotation = 0.0
        self.is_running = True
        self.radars = Radar(-60,radar_batch), Radar(-30,radar_batch), Radar(0,radar_batch), Radar(30,radar_batch), Radar(60,radar_batch)
        self.network = network
        self.last_checkpoint_passed = 0


    def update(self, delta_time):

        render_time = delta_time * 60
        self.speed -= 0.05 #friction
        if self.is_running:
            measurements = [self.probe(radar) / radar.max_length_pixels for radar in self.radars]
            acceleration,steering_position =  self.network.feed_forward(measurements)

            if acceleration > 0:
                self.speed += 0.5

            if self.speed > self.slipping_speed:
                steer_impact = -self.speed / self.max_speed + self.slipping_speed / self.max_speed + 1
            else:
                steer_impact = 1

            self.rotation -= steering_position * self.speed * steer_impact * render_time * 3
        else:
            self.speed -= 0.05 * self.speed * render_time

        if self.speed < 0:
            self.speed = 0
            self.shutdown_engine()

        if self.speed >= self.max_speed:
            self.speed = self.max_speed


        self.body.rotation = -self.rotation
        self.body.x += self.speed * render_time * math.cos(math.radians(self.rotation))
        self.body.y += self.speed * render_time * math.sin(math.radians(self.rotation))

    def probe(self, radar):
        probe_length = 0
        radar.beam.x = self.body.x
        radar.beam.y = self.body.y
        x2 = radar.beam.x
        y2 = radar.beam.y
        while probe_length < radar.max_length_pixels and self.track.is_road(x2, y2):
            probe_length += 2  # pixels
            x2 = self.body.x + probe_length * math.cos(math.radians(self.rotation + radar.angle))
            y2 = self.body.y + probe_length * math.sin(math.radians(self.rotation + radar.angle))
        radar.beam.x2 = x2
        radar.beam.y2 = y2
        return probe_length

    def shutdown_engine(self):
        self.is_running = False
        self.radars = None

    def hit_checkpoint(self, id_):
        if id_ - self.last_checkpoint_passed == 1:
            self.last_checkpoint_passed = id_
        elif id_ < self.last_checkpoint_passed:
            self.shutdown_engine()
