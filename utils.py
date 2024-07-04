from typing import Generator, Tuple, List
import pygame
from objects import Object

pygame.init()

font = pygame.font.Font(None, 16)


def display(objects: List[Object]) -> None:
    for object in objects:
        object.draw()


def debug(objects: List[Object], on_corner: bool = True) -> None:
    n = 10
    for object in objects:
        for force in object.forces:
            force.draw()
        screen = pygame.display.get_surface()
        pos_text = font.render(
            f"x: {object.position.x_component: .2f}, y:{object.position.y_component: .2f}",
            True,
            (255, 0, 0),
        )
        acc_text= font.render(
            f"a: {object.acceleration}", True, (255, 0, 0)
        )
        vel_text = font.render(
            f"v: {object.velocity}", True, (255, 0, 0)
        )
        info_text = font.render(
            f"m: {object.mass}", True, (255, 0, 0)
        )  # add info such as mu and e
        if on_corner:
            screen.blit(pos_text, (800, n + 10))
            screen.blit(acc_text, (800, n + 20))
            screen.blit(vel_text, (800, n + 30))
            screen.blit(info_text, (800, n + 40))
            n += 50
        else:
            screen.blit(
                pos_text, (object.position.x_component, object.position.y_component)
            )
            screen.blit(
                acc_text,
                (object.position.x_component, object.position.y_component + 10),
            )
            screen.blit(
                vel_text,
                (object.position.x_component, object.position.y_component + 20),
            )
            screen.blit(
                info_text,
                (object.position.x_component, object.position.y_component + 30),
            )


def update(objects: List[Object], dt: float) -> None:
    for object in objects:
        if object.fixed:
            continue
        object.update(dt)


def nearby(objects: List[Object]) -> Generator[Tuple[bool, Object, Object], None, None]:
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i == j:
                continue
            if (obj1.position - obj2.position).magnitude() < obj1.extent + obj2.extent:
                yield True, obj1, obj2
            else:
                yield False, obj1, obj2


def check_collision(objects: List[Object]) -> None:
    for is_nearby, obj1, obj2 in nearby(objects):
        if is_nearby:  # i am not sure if this a more effective way to deal or not.
            collision = obj1.collide_with(obj2)
            if collision:  # all collisions are conisdered elastic so far. May add coefficient of restitution later.
                print(f"{obj1} collided with {obj2}")
