import pyvista
import math
import numpy as np

class LunarSimulation:
    def __init__(self):
        self.radius = 1737400  # Radius of the Moon in meters
        self.moon_sphere = None
        self.star_sphere = None

    def create_moon(self):
        self.moon_sphere = pyvista.Sphere(
            radius=self.radius,
            theta_resolution=120,
            phi_resolution=120,
            start_theta=270.001, end_theta=270
        )

    def create_stars(self):
        self.star_sphere = pyvista.Sphere(
            radius=self.radius * 100,  # Large sphere for stars
            theta_resolution=120,
            phi_resolution=120,
            start_theta=270.00001, end_theta=270
        )

    def normalize_points(self, sphere, radius):
        points = sphere.points / radius
        sphere.active_texture_coordinates = np.zeros((sphere.points.shape[0], 2))
        sphere.active_texture_coordinates[:, 0] = 0.5 + np.arctan2(-points[:, 0], points[:, 1]) / (2 * math.pi)
        sphere.active_texture_coordinates[:, 1] = 0.5 + np.arcsin(points[:, 2]) / math.pi

    def load_textures(self):
        moon_texture = pyvista.read_texture("8k_moon.jpg")
        stars_texture = pyvista.read_texture("8k_stars.jpg")
        return moon_texture, stars_texture
    
    def setup_plotter(self, moon_texture, stars_texture):
        pl = pyvista.Plotter()

        pl.add_mesh(self.moon_sphere, texture=moon_texture, smooth_shading=False)
        pl.add_mesh(self.star_sphere, texture=stars_texture, smooth_shading=False)

        # Set starting camera position at equator of the Moon
        pl.camera_position = [(0, self.radius * 4, 0), (0, 0, 0), (0, 0, 1)]

        # Set max zoom level
        pl.camera.zoom(1.5)

        # Set background color to black
        pl.set_background("black")

        return pl

class LunarSimulator():
    def __init__(self):
        self.simulation = LunarSimulation()
        self.moon_radius = 1737400  # Radius of the Moon in meters

    def run(self):

        # Create the Moon and stars
        self.simulation.create_moon()
        self.simulation.create_stars()

        # Normalize points and set up textures
        self.simulation.normalize_points(self.simulation.moon_sphere, self.moon_radius)
        self.simulation.normalize_points(self.simulation.star_sphere, self.moon_radius * 100)
        moon_texture, stars_texture = self.simulation.load_textures()

        # Set up the plotter with textures and camera
        pl = self.simulation.setup_plotter(moon_texture, stars_texture)
        pl.show()

LunarSimulator().run()