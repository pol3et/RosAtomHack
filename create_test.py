import os
import shutil

WIDTH = 960
HEIGHT = 600
BOUNDING_BOX_SIZE = 160
IMG_SIZE = 640

def get_yolo_dataset(file_path, transform=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.replace('\\', '/').replace('.frame', '.bmp').strip() for line in lines]
        miss_list = []
        i = 0
        miss = 0
        countall = 0
        while i < len(lines)-miss:
            line = lines[i]
            from_path = f"./DATASET/FRAMES/{line}"
            countall += 1
            if os.path.exists(from_path):
                print(from_path)
                if transform:
                    transform(from_path)
                index = countall-miss
                to_path_frame = f"./test/images/{index}.bmp"
                to_path_txt = f"./test/labels/{index}.txt"
                os.makedirs(os.path.dirname(to_path_frame), exist_ok=True)
                os.makedirs(os.path.dirname(to_path_txt), exist_ok=True)
                shutil.copy(from_path, to_path_frame)
                i += 1
                
                # Check if all labels are 0 for the current image
                all_labels_zero = True
                with open(to_path_txt, 'w') as label_file:
                    while i < len(lines) and len(lines[i].split(', ')) > 1:
                        x, y, label = map(int, lines[i].split(", "))
                        if label != 0:  # Skip the null class
                            all_labels_zero = False
                            label_file.write(f"{label-1} {x/WIDTH} {y/HEIGHT} {BOUNDING_BOX_SIZE/WIDTH} {BOUNDING_BOX_SIZE/HEIGHT}\n")
                        i += 1

                # If all labels are 0, delete the files and decrement countall
                if all_labels_zero:
                    os.remove(to_path_frame)
                    os.remove(to_path_txt)
                    countall -= 1
            else:
                miss += 1
                i += 1
                miss_list.append(from_path)

    print('Processed:', countall)
    print('Not in dir: ', miss)
    with open('misses_test.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(miss_list))

file_path = 'DATASET/metadata/test_set.txt'
get_yolo_dataset(file_path)