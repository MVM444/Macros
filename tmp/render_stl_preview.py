import os
import struct
import numpy as np
from PIL import Image, ImageDraw

base = os.path.dirname(__file__)
output = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.png"
items = [
    ("puriscal_slab.stl", (190, 174, 145)),
    ("puriscal_wall.stl", (216, 190, 142)),
    ("puriscal_columns.stl", (150, 125, 88)),
]

def triangles(path):
    with open(path, "rb") as stream:
        stream.read(80)
        count = struct.unpack("<I", stream.read(4))[0]
        data = []
        for _ in range(count):
            values = struct.unpack("<12fH", stream.read(50))
            data.append(np.array(values[3:12], dtype=float).reshape(3, 3))
        return data

faces = []
for filename, color in items:
    for tri in triangles(os.path.join(base, filename)):
        faces.append((tri, color))

points = np.concatenate([tri for tri, _ in faces], axis=0)
center = (points.min(axis=0) + points.max(axis=0)) / 2.0
angle_z = np.deg2rad(-38.0)
angle_x = np.deg2rad(58.0)
rz = np.array([[np.cos(angle_z), -np.sin(angle_z), 0], [np.sin(angle_z), np.cos(angle_z), 0], [0, 0, 1]])
rx = np.array([[1, 0, 0], [0, np.cos(angle_x), -np.sin(angle_x)], [0, np.sin(angle_x), np.cos(angle_x)]])
rotation = rz @ rx
rotated = [((tri - center) @ rotation, color) for tri, color in faces]
all_rot = np.concatenate([tri for tri, _ in rotated], axis=0)
xy_min, xy_max = all_rot[:, :2].min(axis=0), all_rot[:, :2].max(axis=0)
width, height, margin = 1400, 1000, 55
scale = min((width - 2 * margin) / max(xy_max[0] - xy_min[0], 1), (height - 2 * margin) / max(xy_max[1] - xy_min[1], 1))

image = Image.new("RGB", (width, height), (238, 241, 246))
draw = ImageDraw.Draw(image)
light = np.array([0.3, -0.4, 0.86]); light /= np.linalg.norm(light)

def screen(point):
    x = margin + (point[0] - xy_min[0]) * scale
    y = height - margin - (point[1] - xy_min[1]) * scale
    return (float(x), float(y))

for tri, color in sorted(rotated, key=lambda item: float(item[0][:, 2].mean())):
    normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
    length = np.linalg.norm(normal)
    shade = 0.72 if length == 0 else 0.65 + 0.35 * abs(float(np.dot(normal / length, light)))
    fill = tuple(max(0, min(255, int(channel * shade))) for channel in color)
    polygon = [screen(point) for point in tri]
    draw.polygon(polygon, fill=fill, outline=(78, 76, 70))

draw.text((32, 24), "Puriscal - Facil Arquitectura", fill=(35, 42, 52))
image.save(output)
print(output)
