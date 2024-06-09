import numpy as np
from scipy.spatial import cKDTree

def average_segment(img, n):
    h, w = img.shape[:2]
    coords = np.random.randint((0, 0), (h, w), (n, 2))

    # Fast nearest neighbor search
    tree = cKDTree(coords)
    grid_points = np.indices((h, w)).reshape(2, -1).T
    _, indices = tree.query(grid_points, k=1)

    groups = [[] for _ in range(n)]
    for i, idx in enumerate(indices):
        groups[idx].append(grid_points[i])

    res = np.zeros_like(img)
    for points in groups:
        if len(points) == 0:
            continue
        points = np.array(points)
        colors = img[points[:, 0], points[:, 1]]
        res[points[:, 0], points[:, 1]] = np.mean(colors, axis=0)
    return res


def center_segment(img, n):
    h, w = img.shape[:2]
    coords = np.random.randint((0, 0), (h, w), (n, 2))

    # Fast nearest neighbor search
    tree = cKDTree(coords)
    grid_points = np.indices((h, w)).reshape(2, -1).T
    _, indices = tree.query(grid_points, k=1)

    colors = img[coords[:, 0], coords[:, 1]]
    nearest_colors = colors[indices]
    return nearest_colors.reshape(h, w, -1)
