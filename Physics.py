import pygame
import pymunk

class Physics():
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 200)
        self.balls = []
        self.static_balls = []
        self.static_lines = []
    
    def create_ball(self, x, y, r):
        body = pymunk.Body(1, 10, body_type = pymunk.Body.DYNAMIC)
        body.position = (x, y)
        shape = pymunk.Circle(body, r)
        shape.density = 0.6
        shape.elasticity = 0.7
        self.space.add(body, shape)
        self.balls.append(shape)
    
    def draw_ball(self, settings, color):
        for ball in self.balls:
            x = int(ball.body.position.x)
            y = int(ball.body.position.y)
            pygame.draw.circle(settings.screen, color, (x, y), ball.radius)
    
    def create_static_ball(self, x, y, r):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = (x, y)
        shape = pymunk.Circle(body, r)
        shape.density = 0.3
        shape.elasticity = 0.2
        self.space.add(body, shape)
        self.static_balls.append(shape)
    
    def draw_static_ball(self, settings, color, extra_y = 0, radius = -1):
        for ball in self.static_balls:
            x = int(ball.body.position.x)
            y = int(ball.body.position.y)
            if radius == -1:
                radius = ball.radius
            if y + extra_y >= y:
                extra_y = 0
            pygame.draw.circle(settings.screen, color, (x, y + extra_y), radius)
    
    def create_static_wall(self, settings, x):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        y = int(settings.screen_size[1])
        shape = pymunk.Segment(body, (x, 0), (x, y), 5)
        shape.elasticity = 0.2
        shape.density - 0.3
        self.space.add(body, shape)
        self.static_lines.append(shape)
    
    def draw_static_wall(self, settings, color):
        for line in self.static_lines:
            x1 = int(line.a[0])
            y1 = int(line.a[1])
            x2 = int(line.b[0])
            y2 = int(line.b[1])
            pygame.draw.line(settings.screen, color, (x1, y1), (x2, y2), 10)
    
    def remove_unused_objects(self, y):
        for ball in self.balls:
            if ball.body.position.y >= y:
                self.space.remove(ball, ball.body)
                self.balls.remove(ball)
    
    def reset_space(self):
        for ball in self.balls:
            self.space.remove(ball, ball.body)
        
        for ball_static in self.static_balls:
            self.space.remove(ball_static, ball_static.body)
        
        for line in self.static_lines:
            self.space.remove(line, line.body)
        
        self.balls.clear()
        self.static_balls.clear()
        self.static_lines.clear()