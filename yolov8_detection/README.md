# yolov8_detection

### 功能說明
對yolov8的detection結果整理為方便存取格式的範例程式
目前的輸入對象是針對單一圖片的偵測結果，想要輸入影片請自行改寫
參考官方文檔: https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
```
$ pip install ultralytics
```
### 使用方法
- 更改輸入圖片路徑: IMG_PATH
- 更改輸出生成圖片結果路徑: SAVE_PATH

```
    IMG_PATH = 'test_img.png'
    SAVE_PATH = 'result.png'
```

### 輸出格式
- 輸出資料儲存在變數prop_list中
- prop_list是一個list包含所有偵測結果
- 每個結果都是一個dictionary包含關鍵字: 'id', 'name', 'conf', 'xyxy'
```
    'id': yolov8偵測結果的預設分類id, 
    'name': id對應的物件名稱, 
    'conf': 該偵測結果的信心分數,
    'xyxy': 偵測結果的Bounding box的左上、右下座標，(x0, y0)、(x1, y1)
```

### 待更新功能:
- [ ] ...
