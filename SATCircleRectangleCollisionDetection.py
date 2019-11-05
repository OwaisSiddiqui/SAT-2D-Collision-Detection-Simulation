import math
import pygame


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt(x ** 2 + y ** 2)


def project_vector(vector1, vector2):
    return get_dot_product(vector1, get_unit_vector(vector2))


def get_dot_product(vector1, vector2):
    return (vector1.x * vector2.x) + (vector1.y * vector2.y)


def get_normal(vector):
    return Vector(vector.y, -vector.x)


def get_vector(point):
    return Vector(point[0], point[1])


def scale_vector(vector, magnitude):
    return Vector(vector.x*magnitude, vector.y*magnitude)


def get_unit_vector(vector):
    if vector.magnitude != 0:
        return scale_vector(vector, 1 / vector.magnitude)
    else:
        return scale_vector(vector, 0)


def get_closest_point(circle_centre, rectangle_points):
    closest_distance = float('inf')
    closest_point = None
    for point in rectangle_points:
        distance = (circle_centre[0] - point[0])**2 + (circle_centre[1] - point[1])**2
        if distance <= closest_distance:
            closest_distance = distance
            closest_point = point
    return closest_point


def is_collision(circle_centre, rectangle_points):
    closest_point = get_closest_point(circle_centre, rectangle_points)
    rectangle_edge_vectors = []
    for point in rectangle_points:
        rectangle_edge_vectors += [get_vector(point)]
    rectangle_edge_normals = []
    for i in range(len(rectangle_points) - 1):
        rectangle_edge_normals += [get_normal(get_vector((rectangle_points[i + 1][0] - rectangle_points[i][0], rectangle_points[i + 1][1] - rectangle_points[i][1])))]
    rectangle_edge_normals += [get_normal(get_vector((rectangle_points[0][0] - rectangle_points[len(rectangle_points) - 1][0], rectangle_points[0][1] - rectangle_points[len(rectangle_points) - 1][1])))]
    rectangle_edge_normals += [get_vector((circle_centre[0] - closest_point[0], circle_centre[1] - closest_point[1]))]
    axes = rectangle_edge_normals
    vectors = rectangle_edge_vectors
    for axis in axes:
        current_rect_max_x = float('-inf')
        current_rect_min_x = float('inf')
        for vector in vectors:
            current_rect_projection = project_vector(vector, axis)
            if current_rect_projection >= current_rect_max_x:
                current_rect_max_x = current_rect_projection
            if current_rect_projection <= current_rect_min_x:
                current_rect_min_x = current_rect_projection
        current_circle_projection = project_vector(get_vector(circle_centre), axis)
        current_circle_max_x = current_circle_projection + 25
        current_circle_min_x = current_circle_projection - 25
        if current_rect_min_x > current_circle_max_x or current_circle_min_x > current_rect_max_x:
            return False
    return True


if __name__ == "__main__":
    # rectangle_points_main = [(250, 250), (300, 250), (300, 300), (300, 250)]
    # circle_centre_main = (230, 340)
    # if is_collision(circle_centre_main, rectangle_points_main):
    #     print("***** COLLISION *****")
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    rectangle_points_main = [(250, 250), (300, 250), (300, 300), (250, 300)]
    rect = (250, 250, 50, 50)
    circle_centre_main = (0, 0)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            circle_centre_main = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        display.fill((255, 255, 255))
        if is_collision(circle_centre_main, rectangle_points_main):
            pygame.draw.circle(display, (255, 0, 0), circle_centre_main, 25)
        else:
            pygame.draw.circle(display, (0, 0, 255), circle_centre_main, 25)
        pygame.draw.rect(display, (0, 255, 0), rect)
        dt = clock.tick(60)
        dt /= 1000
        pygame.display.update()
