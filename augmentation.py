from PIL import Image
import os

def mirror_images(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.bmp'):
            file_path = os.path.join(input_directory, file_name)
            image = Image.open(file_path)

            # Mirror horizontally
            mirrored_horizontal = image.transpose(Image.FLIP_LEFT_RIGHT)
            mirrored_horizontal.save(os.path.join(output_directory, f'mirror_horizontal_{file_name}'))

            # Mirror vertically
            mirrored_vertical = image.transpose(Image.FLIP_TOP_BOTTOM)
            mirrored_vertical.save(os.path.join(output_directory, f'mirror_vertical_{file_name}'))

if __name__ == "__main__":
    input_directory = './healthy_images/'
    output_directory = './augmented_images/'

    mirror_images(input_directory, output_directory)
