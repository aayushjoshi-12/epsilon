import math

import pygame

from constants import GRAVITATIONAL_ACCELERATION as g

pygame.init()

font = pygame.font.Font(None, 16)


class Vector:
    def __init__(self, x_component: float = 0, y_component: float = 0) -> None:
        self.x_component = x_component
        self.y_component = y_component

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(
            self.x_component + other.x_component, self.y_component + other.y_component
        )

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(
            self.x_component - other.x_component, self.y_component - other.y_component
        )

    def __mul__(self, other: float) -> "Vector":
        return Vector(self.x_component * other, self.y_component * other)

    def __truediv__(self, other: float) -> "Vector":
        return Vector(self.x_component / other, self.y_component / other)

    def magnitude(self) -> float:
        return (self.x_component**2 + self.y_component**2) ** 0.5

    def direction(self) -> tuple["Vector", float]:
        mag = self.magnitude()
        if mag != 0:
            return self / mag, math.atan(self.y_component / self.x_component)
        return Vector(0, 0), math.atan(self.y_component / self.x_component)

    def __str__(self) -> str:
        return f"{self.x_component: .2f}î + {self.y_component: .2f}ĵ"


class Force(Vector):
    def __init__(
        self,
        x_component: float,
        y_component: float,
        application_point: Vector,
        constant: bool = True,
    ) -> None:
        super().__init__(x_component, y_component)
        self.constant = constant
        self.tail = Vector(application_point.x_component, application_point.y_component)
        self.head = Vector(
            application_point.x_component + self.x_component,
            application_point.y_component + self.y_component,
        )

    def __add__(self, other: "Force") -> "Force":
        return Force(
            self.x_component + other.x_component,
            self.y_component + other.y_component,
            self.tail,
        )

    def __sub__(self, other: "Force") -> "Force":
        return Force(
            self.x_component - other.x_component,
            self.y_component - other.y_component,
            self.tail,
        )

    def __mul__(self, other: float) -> "Force":
        return Force(self.x_component * other, self.y_component * other, self.tail)

    def __truediv__(self, other: float) -> "Force":
        return Force(self.x_component / other, self.y_component / other, self.tail)

    def draw(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (self.tail.x_component, self.tail.y_component),
            (self.head.x_component, self.head.y_component),
            1,
        )
        mag = self.magnitude()
        text = font.render(f"{mag: .2f}", True, (255, 0, 0))
        screen.blit(text, (self.head.x_component, self.head.y_component - 10))

    def update(self, new_application_point) -> None:
        self.tail = new_application_point
        self.head = Vector(
            new_application_point.x_component + self.x_component,
            new_application_point.y_component + self.y_component,
        )


class GravitationalForce(Force):
    def __init__(self, mass: float, application_point: Vector) -> None:
        super().__init__(0, mass * g, application_point)
