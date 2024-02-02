import os
import shutil


def copy_one_layer_subdir_filter(root: str, target: str, drop_ext: str):
    '''
        filter will drop files with drop_extend
    '''
    sub_dirs = sorted(os.listdir(ROOT_DIR))
    read_dirs_path = [os.path.join(ROOT_DIR, d) for d in sub_dirs]
    save_dirs_path = [os.path.join(TARGET_DIR, d) for d in sub_dirs]

    for i in range(len(read_dirs_path)):
        os.makedirs(save_dirs_path[i], exist_ok=True)

        for file in os.listdir(read_dirs_path[i]):
            if file.endswith(drop_ext) and file.startswith('kps'):
                source_path = os.path.join(read_dirs_path[i], file)
                target_path = os.path.join(save_dirs_path[i], file)

                shutil.copy(source_path, target_path)
        print('id {} done'.format(read_dirs_path[i]))


if __name__ == "__main__":
    ROOT_DIR = "./dataset_xyz_8736"
    TARGET_DIR = "./download_8736_only_kps"

    copy_one_layer_subdir_filter(ROOT_DIR, TARGET_DIR, drop_ext='.json')
