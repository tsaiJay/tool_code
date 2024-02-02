import os
import shutil
from tqdm import tqdm


def copy_data(source_path: str, target_path: str):
    # if not os.path.exists(target_path_should_be_dir_name):
    #     os.makedirs(target_path, exist_ok=True)
    shutil.copy(source_path, target_path)


def copy_dir(source: str, target: str):
    shutil.copytree(source_path, target_path)


if __name__ == "__main__":
    TARGET_LIST = ['./1_20240120_trajectory_4043_XYZ',
                   './2_20240121_trajectory_1253_XYZ',
                   './3_20240122_trajectory_1020_XYZ',
                   './4_20240122_trajectory_1020_noon_XYZ',
                   './5_20240123_trajectory_1400_XYZ']
    OUTPUT_DIR = './output_xyz'

    sample_num = 0
    for folder in TARGET_LIST:
        sample_num += len(os.listdir(folder))
    print('total samples:', sample_num)

    all_sub_dir = []
    for parent_dir in TARGET_LIST:
        sub_dir = sorted(os.listdir(parent_dir))
        path_list = [os.path.join(parent_dir, d) for d in sub_dir]
        all_sub_dir += path_list
    # print(all_sub_dir, len(all_sub_dir))

    for idx in tqdm(range(sample_num)):
        source_path = all_sub_dir[idx]
        target_path = os.path.join(OUTPUT_DIR, '{:05d}'.format(idx))

        copy_dir(source_path, target_path)
