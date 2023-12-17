import torch
from torchvision.utils import save_image
from PIL import Image
import numpy as np
import os
from torchvision import transforms
from model import Generator, Encoder
import tqdm

def calculate_mask_for_image(opt, input_image_path, img_idx, set='train'):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    generator = Generator(opt)
    encoder = Encoder(opt)

    generator.load_state_dict(torch.load("results/generator", map_location=device))
    encoder.load_state_dict(torch.load("results/encoder", map_location=device))

    generator.to(device).eval()
    encoder.to(device).eval()

    transform = transforms.Compose([
        transforms.Resize([opt.img_size] * 2),
        transforms.ToTensor(),
        transforms.Normalize([0.5] * opt.channels, [0.5] * opt.channels)
    ])

    input_image = Image.open(input_image_path).convert('RGB')
    input_image_original_size = np.array(input_image)  # Save the original size
    input_image = transform(input_image).unsqueeze(0).to(device)

    with torch.no_grad():
        real_z = encoder(input_image)
        reconstructed_img = generator(real_z)

    original_image_np = input_image.squeeze().cpu().numpy()
    reconstructed_image_np = reconstructed_img.squeeze().cpu().numpy()
    difference = np.abs(original_image_np - reconstructed_image_np)
    normalized_difference = difference / np.max(difference)
    threshold = 0.69
    mask = normalized_difference > threshold

    mask_resized = (mask * 255).astype(np.uint8)

    mask_resized = mask_resized[0] + mask_resized[1] + mask_resized[2]
    mask_resized = Image.fromarray(mask_resized, mode='L').resize((960, 600), Image.NEAREST)

    if set == 'train':
        os.makedirs("results/masks_train", exist_ok=True)
        mask_resized.save(f"results/masks_train/{img_idx}.png")

    elif set == 'test':
        os.makedirs("results/masks_test", exist_ok=True)
        mask_resized.save(f"results/masks_test/{img_idx}.png")

    else:
        raise ValueError(f"Unknown set {set}")

    return mask_resized


import argparse
opt = argparse.Namespace(
    test_root='results/train/class0/images',
    n_grid_lines=10,
    latent_dim=100,
    img_size=64,
    channels=3,
    n_iters=None
)

for i in range(1, 4238):
    input_image_path = f"train/images/class0/{i}.bmp"
    calculate_mask_for_image(opt, input_image_path, i, set='train')
    tqdm.tqdm.write(f"Processed {i} images in train")

opt = argparse.Namespace(
    test_root='results/test/class0/images',
    n_grid_lines=10,
    latent_dim=100,
    img_size=64,
    channels=3,
    n_iters=None
)

for i in range(1, 2225):
    input_image_path = f"test/images/class0/{i}.bmp"
    calculate_mask_for_image(opt, input_image_path, i, set='test')
    tqdm.tqdm.write(f"Processed {i} images in test")