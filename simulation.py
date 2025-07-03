import pyvista
import math
import numpy as np

radius = 1737400  # Radius of the Moon in meters

sphere = pyvista.Sphere(
    radius=radius,
    theta_resolution=120,
    phi_resolution=120,
    start_theta=270.001, end_theta=270
)

# Normalize to unit sphere for UV mapping
points = sphere.points / radius

sphere.active_texture_coordinates = np.zeros((sphere.points.shape[0], 2))
sphere.active_texture_coordinates[:, 0] = 0.5 + np.arctan2(-points[:, 0], points[:, 1]) / (2 * math.pi)
sphere.active_texture_coordinates[:, 1] = 0.5 + np.arcsin(points[:, 2]) / math.pi

moon = pyvista.read_texture("moon.jpg")
pl = pyvista.Plotter()
pl.add_mesh(sphere, texture=moon, smooth_shading=False)
pl.show()
