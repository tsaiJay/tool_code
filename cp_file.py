import os
import shutil
from pprint import pprint

def copy_one_layer_subdir(root: str, target: str):
    sub_dirs = sorted(os.listdir(root))
    read_dirs = [os.path.join(root, d) for d in sub_dirs]
    save_dirs = [os.path.join(target, d) for d in sub_dirs]

    for i in range(len(read_dirs)):
        os.makedirs(save_dirs[i], exist_ok=True)

        for f in os.listdir(read_dirs[i]):

            # ==== <CONDITION START> ==== add filter condition here!
            if not f.startswith('log_'):
                continue
            # ==== <CONDITION END> ====

            source_path = os.path.join(read_dirs[i], f)
            target_path = os.path.join(save_dirs[i], f)
            shutil.copy(source_path, target_path)
            # print(source_path, target_path)

        print('id {} done'.format(read_dirs[i]))


if __name__ == "__main__":
    ROOT_DIR = "./dataset_xyz_8736"
    TARGET_DIR = "./new_dataset_xyz_8736"

    copy_one_layer_subdir(ROOT_DIR, TARGET_DIR)
