# Issues

- still some bugs in collision handling for rectangles.
  - i think the reason for that is the slower object collides again giving it a crazy spike in velovity

- the maths that we calculated is not working for circle objects but seems to be working fine for rectangle objects even though we are just updating the inherited properties from objects

- another issue is that nearby function is still not working properly for surface object

- i dont think we need the surface object since we can just use a rectangle with infinite mass and no forces

- the rod object is tricky to handle to collisions with it

# Solved:

- we are calculating the collision twice since each body does that twice but its fine because as soon as we collide something we update its velocity and stuff which makes them away oreventing the second collision from counting