import numpy as np
import cv2 as cv
import base64
from PIL import Image
import io

def process(value):

    x = 6
    y = 3
    box = 1

    decoded_data = base64.b64decode(value)
    np_data = np.fromstring(decoded_data, np.uint8)

    img = cv.imdecode(np_data, cv.IMREAD_UNCHANGED)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_result = cv.resize(img, (600, 300))
    img_new = np.uint8([[[0, 0, 0]]])

    for i in range(0, y):
        for j in range(0, x):
            img_new = cv.rectangle(img_result, (0, i * 100),
                                ((j + 1) * 100, (i + 1) * 100), (0, 0, 0), 1)
            cropped_box = img_new[i * 100:(i + 1) * 100, j * 100: (j + 1) * 100]
            cv.putText(cropped_box, str(box), (10, 20),
                       cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)
            box = box + 1

    pil_img = Image.fromarray(img_new)
    buff = io.BytesIO()
    pil_img.save(buff, format("PNG"))
    img_str = base64.b64encode(buff.getvalue())

    print(img_str)

    return ""+str(img_str,'utf-8')




