import cv2
from ultralytics import YOLO


def save_detection_result(img, prop_list, save_path):
    color = (0, 0, 255)
    thick = 1
    text_size = 0.6
    show_img = img.copy()
    for p in prop_list:
        upper_left = (int(p['xyxy'][0]), int(p['xyxy'][1]))
        lower_right = (int(p['xyxy'][2]), int(p['xyxy'][3]))

        show_img = cv2.rectangle(show_img, upper_left, lower_right, color, thick)
        cv2.putText(
            show_img, '{}/{:.4f}'.format(p['name'], p['conf']), upper_left,
            cv2.FONT_HERSHEY_SIMPLEX, text_size, color, 1, cv2.LINE_AA
        )

    cv2.imwrite(save_path, show_img)


if __name__ == "__main__":
    IMG_PATH = 'test_img.png'
    SAVE_PATH = 'result.png'

    img = cv2.imread(IMG_PATH)

    model = YOLO('yolov8n.pt')  # load an official model

    name_dict = model.names  # get all default class names to a dictionary

    results = model(img, verbose=False)
    # results = model(img, classes=[0], verbose=False)  # only get results from class_id=0(person)

    detects = results[0].boxes  # for the detection task, use ".boxes"

    prop_list = []
    for i in range(len(detects.xywh)):
        prop_list.append({
            'id': detects.cls.tolist()[i],
            'name': name_dict[detects.cls.tolist()[i]],
            'conf': detects.conf.tolist()[i],
            'xyxy': detects.xyxy.tolist()[i]
        })

    from pprint import pprint
    print('all detection results store in a list of adictionaries with key(id, name, conf, xywh)')
    print('-' * 30)
    pprint(prop_list)

    save_detection_result(img, prop_list, SAVE_PATH)
