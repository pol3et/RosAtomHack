import os
import shutil

def collect_healthy_images(file_path, output_directory):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.replace('\\', '/').replace('.frame', '.bmp').strip() for line in lines]
    
    labeled_images = set(line.split('/')[-1] for line in lines)

    for root, dirs, files in os.walk('./DATASET/FRAMES/'):
        for file in files:
            if file.endswith('.bmp') and file not in labeled_images:
                from_path = os.path.join(root, file)
                to_path = os.path.join(output_directory, file)
                
                shutil.copy(from_path, to_path)

if __name__ == "__main__":
    set_file_path = 'DATASET/metadata/set.txt'
    test_set_file_path = 'DATASET/metadata/test_set.txt'
    output_directory = './healthy_images/'

    os.makedirs(output_directory, exist_ok=True)

    collect_healthy_images(set_file_path, output_directory)
    collect_healthy_images(test_set_file_path, output_directory)