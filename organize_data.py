import os
import shutil
import argparse
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-n', '--num-samples', type=int, help='number of samples', default=-1)
    args = parser.parse_args()
    return args


def get_all_file_dict(clients_path: list) -> dict:
    '''
        -output_dict
            'root/client_1/audio-audio' : [audio_files_path_list]
            'root/client_1/video-video' : [video_files_path_list]
            'root/client_1/audio-data' : [json_files_path_list]
            'root/client_2/audio-audio' : [audio_files_path_list]
            ....
    '''
    files_dict = {}
    for client in clients_path:
        aud_vid_dir = [os.path.join(client, folder) for folder in os.listdir(client)]
        
        for folder in aud_vid_dir:
            if 'audio' in os.path.basename(folder):
                temp_audios = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('audio')])
                temp_datas = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('data')])
                
                files_dict[folder + '-audio'] = temp_audios
                files_dict[folder + '-data'] = temp_datas

            if 'video' in os.path.basename(folder):
                temp_videos = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('video')])
                
                files_dict[folder + '-video'] = temp_videos
    # for k in files_dict.keys():
    #     print(k)
    return files_dict


def check_file_correspond(files_dict: dict) -> int:
    len_list = []  # record video-audio-data length
    print('all keys in files_dict, and files_number')
    for k in files_dict.keys():
        print(k, '  ---->    ', len(files_dict[k]))
        len_list.append(len(files_dict[k]))

    assert all(t == len_list[0] for t in len_list), 'audio-video-data number not the same'
    print('    -->>>> data number valid!')

    sample_count = len_list[0]
    return sample_count


if __name__ == '__main__':
    args = get_args()

    '''
        FOLDER STRUCTURE:
        
        -datas
            -client1
                -audio
                -video
            -client2
                -audio_150
                -audio_50
                -video
            -client3
                -audio
                -video
    '''

    ROOT_PATH = "./"
    OUTPUT_PATH = './output'
    SAMPLE_NUM = args.num_samples
    CLIENTS = ['client1', 'client2', 'client3']

    clients_path = [os.path.join(ROOT_PATH, folder) for folder in CLIENTS]

    all_files_dict = get_all_file_dict(clients_path)

    sample_count = check_file_correspond(all_files_dict)

    if SAMPLE_NUM == -1:  # not setting
        SAMPLE_NUM = sample_count

    # === organize files ===
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for idx in tqdm(range(SAMPLE_NUM)):
        target_dir = os.path.join(OUTPUT_PATH, f"{idx:05d}")
        os.makedirs(target_dir, exist_ok=True)

        for k in all_files_dict.keys():
            source_path = all_files_dict[k][idx]
            source_name = os.path.basename(all_files_dict[k][idx])
            target_path = os.path.join(target_dir, source_name)
            
            shutil.copy(source_path, target_path)
            # print(all_files_dict[k][idx], target_path)
