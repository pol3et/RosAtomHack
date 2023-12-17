import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def load_old_clusters(file_path):
    """
    Load old clusters from a label file.

    Parameters:
    - file_path: Path to the label file.

    Returns:
    - List of clusters, each represented as a tuple (label, x_center, y_center, width, height).
    """
    clusters = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            label, x_center, y_center, width, height = map(float, parts)
            clusters.append((label, x_center, y_center, width, height))
    return clusters

def write_new_clusters(file_path, new_clusters):
    """
    Write new clusters to a label file.

    Parameters:
    - file_path: Path to the output label file.
    - new_clusters: List of new clusters, each represented as a tuple (label, x_center, y_center, width, height).
    """
    with open(file_path, 'w') as file:
        for cluster in new_clusters:
            file.write(f"{cluster[0]} {cluster[1]} {cluster[2]} {cluster[3]} {cluster[4]}\n")

def find_clusters_in_mask(mask, old_label_path, max_distance=70):
    """
    Find clusters in a binary mask using k-means algorithm.

    Parameters:
    - mask: Binary mask.
    - old_label_path: Path to the old label file.
    - max_distance: Maximum distance between pixels to consider them part of the same cluster.

    Returns:
    - List of clusters, each represented as a tuple (x_center, y_center, width, height).
    """
    coordinates = np.column_stack(np.nonzero(mask))

    if len(coordinates) == 0:
        return []  # No clusters if no nonzero values

    old_clusters = load_old_clusters(old_label_path)
    clusters_count = len(old_clusters)
    
    try:
        kmeans = KMeans(n_clusters=clusters_count, init='k-means++', max_iter=300, random_state=42, n_init=10)
        kmeans.fit(coordinates)

        cluster_centers = kmeans.cluster_centers_

        clusters = []
        for center in cluster_centers:
            try:
                x_center, y_center = center
            except ValueError:
                continue  # Skip if not enough values to unpack

            cluster_mask = np.sqrt(np.sum((coordinates - center)**2, axis=1)) <= max_distance
            cluster_indices = np.where(cluster_mask)

            if len(cluster_indices[0]) == 0:
                continue  # Skip if no nonzero values in cluster_mask

            cluster_coords = coordinates[cluster_indices]
            min_x, max_x = np.min(cluster_coords[:, 1]), np.max(cluster_coords[:, 1])
            min_y, max_y = np.min(cluster_coords[:, 0]), np.max(cluster_coords[:, 0])
            width = max_x - min_x
            height = max_y - min_y
            x_center = min_x + width // 2
            y_center = min_y + height // 2
            clusters.append((x_center, y_center, width, height))
    except Exception as e:
        print("Error during clustering:", e)
        clusters = []

    return clusters

def process_mask_clusters(idx, mask_path, old_label_path, new_label_path):
    """
    Process clusters in a mask and update the label file.

    Parameters:
    - idx: Index of the mask.
    - mask_path: Path to the mask image.
    - old_label_path: Path to the old label file.
    - new_label_path: Path to the new label file.
    """
    mask = np.array(Image.open(mask_path).convert('L'))  # Convert to grayscale
    clusters_in_mask = find_clusters_in_mask(mask, old_label_path)

    old_clusters = load_old_clusters(old_label_path)
    new_clusters = []

    for mask_cluster in clusters_in_mask:
        x_mask, y_mask, w_mask, h_mask = mask_cluster
        for cluster in old_clusters:
            label, x_center, y_center, width, height = cluster
            x_center /= WIDTH
            y_center /= HEIGHT
            width /= WIDTH
            height /= HEIGHT

            if (x_center >= x_mask - w_mask/2 and x_center <= x_mask + w_mask/2
                    and y_center >= y_mask - h_mask/2 and y_center <= y_mask + h_mask/2):
                new_clusters.append((label, x_mask, y_mask, w_mask, h_mask))
                break

    write_new_clusters(new_label_path, new_clusters)

WIDTH = 960
HEIGHT = 600

for i in range(1, 4238):
    mask_path = f'results/masks_train/{i}.png'
    old_label_path = f'train/labels/{i}.txt'
    new_label_path = f'train/new_labels/{i}.txt'
    process_mask_clusters(i, mask_path, old_label_path, new_label_path)
    print(f"Processed {i} masks in train")

for i in range(1, 2225):
    mask_path = f'results/masks_test/{i}.png'
    old_label_path = f'test/labels/{i}.txt'
    new_label_path = f'test/new_labels/{i}.txt'
    process_mask_clusters(i, mask_path, old_label_path, new_label_path)
    print(f"Processed {i} masks in test")