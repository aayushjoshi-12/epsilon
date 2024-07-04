from typing import List, Tuple, Union
import pygame
from vectors import Force, GravitationalForce, Vector
from constants import screen_width, dt
from constants import COEFFICIENT_OF_RESTITUTION as e

font = pygame.font.Font(None, 16)


class Object:
    def __init__(
        self,
        position: Vector,
        mass: float,
        color: Tuple[int, int, int] = (255, 255, 255),
        fixed: bool = False,
    ) -> None:
        self.position = position
        self.mass = mass
        self.fixed = fixed
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.forces: List[Force] = [GravitationalForce(self.mass, self.position)]
        self.color = color

    def apply_force(self, force: Force) -> None:
        self.forces.append(force)

    def apply_forces(self, forces: List[Force]) -> None:
        self.forces.extend(forces)

    def update(self, dt: float) -> None:
        net_force = Force(0, 0, self.position)
        constant_forces: List[Force] = []
        for force in self.forces:
            net_force += force
            if force.constant:
                constant_forces.append(force)
            force.update(self.position)
        self.acceleration = net_force / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.forces = constant_forces


class Rectangle(Object):
    def __init__(
        self,
        position: Vector,
        mass: float,
        width: float,
        height: float,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(position, mass, color)
        self.width = width
        self.height = height
        self.extent = (self.width**2 + self.height**2) ** 0.5

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        edges_xywh: Tuple[float, float, float, float] = (
            self.position.x_component - self.width / 2,
            self.position.y_component - self.height / 2,
            self.width,
            self.height,
        )
        pygame.draw.rect(screen, self.color, edges_xywh)

    def collide_with(
        self, other: Union["Rectangle", "Circle", "Rod", "Surface"]
    ) -> bool:
        return other.collide_rectangle(self)

    def collide_rectangle(self, rectangle: "Rectangle") -> bool:
        x1 = self.position.x_component - self.width / 2
        y1 = self.position.y_component - self.height / 2
        x2 = self.position.x_component + self.width / 2
        y2 = self.position.y_component + self.height / 2

        a1 = rectangle.position.x_component - rectangle.width / 2
        b1 = rectangle.position.y_component - rectangle.height / 2
        a2 = rectangle.position.x_component + rectangle.width / 2
        b2 = rectangle.position.y_component + rectangle.height / 2

        if (x1 <= a2 and x2 >= a1) and (y1 <= b2 and y2 >= b1):
            vel_a_n = self.velocity.x_component  # velocity before collision
            vel_b_n = rectangle.velocity.x_component
            self.velocity.x_component = ((self.mass - e * rectangle.mass) * vel_a_n) + (
                (1 + e) * rectangle.mass * vel_b_n
            ) / (self.mass + rectangle.mass)
            rectangle.velocity.x_component = (
                (rectangle.mass - e * self.mass) * vel_b_n
            ) + ((1 + e) * self.mass * vel_a_n) / (self.mass + rectangle.mass)
            rectangle.update(dt)
            return True
        return False

    def collide_surface(self, surface: "Surface") -> None:
        pass

    def collide_circle(self, circle: "Circle") -> None:
        pass

    def collide_rod(self, rod: "Rod") -> None:
        pass

    def __str__(self) -> str:
        return "Rectangle"


class Circle(Object):
    def __init__(
        self,
        position: Vector,
        mass: float,
        radius: float,
        color: Tuple[float, float, float] = (255, 255, 255),
    ) -> None:
        super().__init__(position, mass, color)
        self.radius = radius
        self.extent = radius

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.circle(
            screen,
            self.color,
            (self.position.x_component, self.position.y_component),
            self.radius,
        )

    def collide_with(
        self, other: Union["Rectangle", "Circle", "Rod", "Surface"]
    ) -> bool:
        return other.collide_circle(self)

    def collide_rectangle(self, rectangle: "Rectangle") -> None:
        pass

    def collide_surface(self, surface: "Surface") -> None:
        pass

    def collide_circle(self, circle: "Circle") -> bool:
        if (self.position - circle.position).magnitude() <= self.radius + circle.radius:
            vel_a_n = self.velocity.x_component  # velocity before collision
            vel_b_n = circle.velocity.x_component
            self.velocity.x_component = ((self.mass - e * circle.mass) * vel_a_n) + (
                (1 + e) * circle.mass * vel_b_n
            ) / (self.mass + circle.mass)
            circle.velocity.x_component = ((circle.mass - e * self.mass) * vel_b_n) + (
                (1 + e) * self.mass * vel_a_n
            ) / (self.mass + circle.mass)
            circle.update(dt)
            return True
        return False

    def collide_rod(self, rod: "Rod") -> None:
        pass

    def __str__(self) -> str:
        return "Circle"


class Rod(Object):
    def __init__(
        self,
        position: Vector,
        mass: float,
        length: float,
        angle: float = 0,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(position, mass, color)
        self.length = length
        self.angle = angle
        self.extent = length

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        start = self.position.x_component, self.position.y_component
        end = self.position.x_component + self.length, self.position.y_component
        pygame.draw.line(screen, self.color, start, end, 3)

    def collide_with(
        self, other: Union["Rectangle", "Circle", "Rod", "Surface"]
    ) -> bool:
        return other.collide_rod(self)

    def collide_rectangle(self, rectangle: "Rectangle") -> None:
        pass

    def collide_surface(self, surface: "Surface") -> None:
        pass

    def collide_circle(self, circle: "Circle") -> None:
        pass

    def collide_rod(self, rod: "Rod") -> None:
        pass

    def __str__(self) -> str:
        return "Rod"


class Surface(Rectangle):
    def __init__(
        self,
        position: Vector,
        mass: float = 1e10,
        width: float = screen_width,
        height: float = 50,
        fixed: bool = True,
        color: Tuple[int, int, int] = (128, 128, 128),
    ) -> None:
        super().__init__(position, mass, width, height, color)
        self.fixed = fixed

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        edges_xywh: Tuple[float, float, float, float] = (
            self.position.x_component - self.width / 2,
            self.position.y_component - self.height / 2,
            self.width,
            self.height,
        )
        pygame.draw.rect(screen, self.color, edges_xywh)

    def collide_with(
        self, other: Union["Rectangle", "Circle", "Rod", "Surface"]
    ) -> bool:
        return other.collide_surface(self)

    def collide_rectangle(self, rectangle: "Rectangle") -> bool:
        x1 = self.position.x_component - self.width / 2
        y1 = self.position.y_component - self.height / 2
        x2 = self.position.x_component + self.width / 2
        y2 = self.position.y_component + self.height / 2

        a1 = rectangle.position.x_component - rectangle.width / 2
        b1 = rectangle.position.y_component - rectangle.height / 2
        a2 = rectangle.position.x_component + rectangle.width / 2
        b2 = rectangle.position.y_component + rectangle.height / 2

        if (x1 <= a2 and x2 >= a1) and (y1 <= b2 and y2 >= b1):
            vel_a_n = self.velocity.x_component  # velocity before collision
            vel_b_n = rectangle.velocity.x_component
            self.velocity.x_component = ((self.mass - e * rectangle.mass) * vel_a_n) + (
                (1 + e) * rectangle.mass * vel_b_n
            ) / (self.mass + rectangle.mass)
            rectangle.velocity.x_component = (
                (rectangle.mass - e * self.mass) * vel_b_n
            ) + ((1 + e) * self.mass * vel_a_n) / (self.mass + rectangle.mass)
            return True
        return False

    def collide_surface(self, surface: "Surface") -> None:
        pass

    def collide_circle(self, circle: "Circle") -> None:
        pass

    def collide_rod(self, rod: "Rod") -> None:
        pass

    def __str__(self) -> str:
        return "Surface"
