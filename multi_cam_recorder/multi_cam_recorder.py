import cv2
import os


def add_marker(image):
    offset = 60
    img = image.copy()
    img = cv2.circle(img, (320, 240), 3, (0, 255, 0), 1)
    img = cv2.circle(img, (320 + offset, 240), 3, (0, 255, 0), 1)
    img = cv2.circle(img, (320 - offset, 240), 3, (0, 255, 0), 1)
    img = cv2.circle(img, (320, 240 + offset), 3, (0, 255, 0), 1)
    img = cv2.circle(img, (320, 240 - offset), 3, (0, 255, 0), 1)
    return img


def show_window_process(window_height, imgs):
    img_1 = cv2.hconcat([add_marker(imgs[0]), add_marker(imgs[1])])
    img_2 = cv2.hconcat([add_marker(imgs[1]), add_marker(imgs[1])])
    show_img = cv2.vconcat([img_1, img_2])
    show_ratio = 480 / show_img.shape[0]  # show height
    show_img = cv2.resize(show_img, (int(show_img.shape[1] * show_ratio), int(show_img.shape[0] * show_ratio)))
    cv2.putText(show_img, 'RECORD : ' + str(is_record), (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    cv2.putText(show_img, 'key : start(S)  pause(P)  stop(N)  quit(Q)', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

    return show_img


class MultiCamManager(object):

    def __init__(self, cam_ids: list, save_dir: str, attr: dict):

        self.save_dir = save_dir
        self.cam_num = len(cam_ids)
        self.cam_list = self.startup_cam(cam_ids)
        self.attr = attr

        self.set_attri(self.attr)
        self.print_info()

    def print_info(self):
        for i in range(self.cam_num):
            w = int(self.cam_list[i].get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.cam_list[i].get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.cam_list[i].get(cv2.CAP_PROP_FPS)
            print('cam{} fps:{:3.2f}  resolution:({:4d},{:4d})'.format(i, fps, w, h))

    def startup_cam(self, cam_ids: list) -> list:
        cam_list = []
        for i in range(self.cam_num):
            cam_list.append(cv2.VideoCapture(cam_ids[i], cv2.CAP_DSHOW))
            assert cam_list[i].isOpened(), "camID{} cannot open".format(cam_ids[i])
        return cam_list

    def set_attri(self, attr):
        self.fps = self.attr['fps']
        self.reso = self.attr['resolution']

        assert self.reso in [480, 720, 1080], 'resolution setting not accept'
        if self.reso == 480:
            w, h = 640, 480
        elif self.reso == 720:
            w, h = 1280, 720
        elif self.reso == 1080:
            w, h = 1920, 1080
        self.w, self.h = w, h

        for i in range(self.cam_num):
            self.cam_list[i].set(cv2.CAP_PROP_FPS, self.fps)
            self.cam_list[i].set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
            self.cam_list[i].set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
            # self.cam_list[i].set(cv2.CAP_PROP_EXPOSURE, -5)
            # self.cam_list[i].set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            assert self.w == self.cam_list[i].get(cv2.CAP_PROP_FRAME_WIDTH), 'cam{} w:{} setup failure'.format(i, self.w)
            assert self.h == self.cam_list[i].get(cv2.CAP_PROP_FRAME_HEIGHT), 'cam{} h:{} setup failure'.format(i, self.h)

    def build_writer(self) -> int:
        new_vid_id = self.get_save_idx(self.save_dir)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writters = []
        for i in range(self.cam_num):
            self.cam_list[i].set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.video_writters.append(cv2.VideoWriter(
                self.save_dir + 'vid{}_cam{}.mp4'.format(new_vid_id, i), fourcc, self.fps, (self.w, self.h))
            )
        return new_vid_id

    def read_frame(self) -> list:
        frames = []
        for i in range(self.cam_num):
            ret, frame = self.cam_list[i].read()
            if ret is True:
                frames.append(frame)
        return frames

    def write_frame(self, frames):
        for i in range(self.cam_num):
            self.video_writters[i].write(frames[i])

    def release(self):
        for i in range(self.cam_num):
            self.cam_list[i].release()

    def get_save_idx(self, scan_dir: str) -> int:
        files = os.listdir(scan_dir)
        vids = [f for f in files if f.endswith(".mp4")]
        if len(vids) == 0:
            return 0
        current_idx = sorted([int(n.split('_')[0][3:]) for n in vids])[-1]
        return current_idx + 1


if __name__ == "__main__":

    SAVE_DIR = './shoot_multi_vid/'
    CAM_ID = [0, 1]
    ATTRIBUTE = {
        'fps': 30,  # maximum of fps depends on hardware
        'resolution': 480,  # 480 or 720 or 1080, which might depend on hardware
    }

    cams = MultiCamManager(cam_ids=CAM_ID, save_dir=SAVE_DIR, attr=ATTRIBUTE)

    turn_off = False
    while turn_off is False:

        is_record = False
        new_vid_id = cams.build_writer()
        print('---> current record video file ID: ', new_vid_id)

        while True:
            frames = cams.read_frame()

            show_img = show_window_process(window_height=480, imgs=frames)

            cv2.imshow('Frame', show_img)

            if is_record is True:
                cams.write_frame(frames)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('s'):  # start record
                is_record = True
            if key == ord('p'):  # pause
                is_record = False
            if key == ord('n'):  # save and create new video
                break
            if key == ord('q'):  # exit program
                turn_off = True
                break

    cv2.destroyAllWindows()
