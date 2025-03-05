"""
This script demonstrates basic turtle graphics operations.
"""

from turtle import Turtle, Screen


def draw_polygon(t, sides, length):
    """
    Draws a polygon with the specified number of sides and side length.
    :param t: The turtle instance
    :param sides: Number of sides of the polygon (e.g., 3 for triangle, 4 for square)
    :param length: Length of each side
    """
    angle = 360 / sides  # Calculate the angle between each side

    for _ in range(sides):
        t.forward(length)
        t.right(angle)


# Create a turtle screen object
SCREEN = Screen()
SCREEN.bgcolor("white")  # Set the background color

# Create a turtle instance
t = Turtle()
t.speed(2)
t.shape("turtle")
t.color("blue")

# Draw a square (for example, you can change sides to draw other polygons)
draw_polygon(t, 4, 100)

# Hide the turtle and display the window
t.hideturtle()
SCREEN.mainloop()
