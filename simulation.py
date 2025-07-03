import pyvista
import math
import numpy as np

radius = 1737400  # Radius of the Moon in meters

moon_sphere = pyvista.Sphere(
    radius=radius,
    theta_resolution=120,
    phi_resolution=120,
    start_theta=270.001, end_theta=270
)

star_sphere = pyvista.Sphere(
    radius=radius * 100,  # Large sphere for stars
    theta_resolution=120,
    phi_resolution=120,
    start_theta=270.00001, end_theta=270
)

# Normalize to unit sphere for UV mapping
moon_points = moon_sphere.points / radius

star_points = star_sphere.points / (radius * 100)

moon_sphere.active_texture_coordinates = np.zeros((moon_sphere.points.shape[0], 2))
moon_sphere.active_texture_coordinates[:, 0] = 0.5 + np.arctan2(-moon_points[:, 0], moon_points[:, 1]) / (2 * math.pi)
moon_sphere.active_texture_coordinates[:, 1] = 0.5 + np.arcsin(moon_points[:, 2]) / math.pi

star_sphere.active_texture_coordinates = np.zeros((star_sphere.points.shape[0], 2))
star_sphere.active_texture_coordinates[:, 0] = 0.5 + np.arctan2(-star_points[:, 0], star_points[:, 1]) / (2 * math.pi)
star_sphere.active_texture_coordinates[:, 1] = 0.5 + np.arcsin(star_points[:, 2]) / math.pi

# Load textures
moon = pyvista.read_texture("8k_moon.jpg")
stars = pyvista.read_texture("8k_stars.jpg")

pl = pyvista.Plotter()

pl.add_mesh(moon_sphere, texture=moon, smooth_shading=False)
pl.add_mesh(star_sphere, texture=stars, smooth_shading=False)

# Set starting camera position at equator of the Moon
pl.camera_position = [(0, radius * 4, 0), (0, 0, 0), (0, 0, 1)]

# Set max zoom level
pl.camera.zoom(1.5)

# Set background color to black
pl.set_background("black")

pl.show()
