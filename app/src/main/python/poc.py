import numpy as np
import cv2 as cv
import base64
from os.path import dirname, join

def nilaiPOC(value):
    arrValue = value.split(",")

    decoded_data1 = base64.b64decode(arrValue[0])
    decoded_data2 = base64.b64decode(arrValue[1])

    print('gambar 1 : ', decoded_data1)
    print('gambar 2 : ', decoded_data2)

    np_data1 = np.fromstring(decoded_data1, np.uint8)
    np_data2 = np.fromstring(decoded_data2, np.uint8)

    img1 = cv.imdecode(np_data1,cv.IMREAD_UNCHANGED)
    img2 = cv.imdecode(np_data2,cv.IMREAD_UNCHANGED)

    img1_array = np.array(img1)
    img2_array = np.array(img2)

    G_a = np.fft.fft2(img1_array)
    G_b = np.fft.fft2(img2_array)
    conj_b = np.ma.conjugate(G_b)
    R = G_a * conj_b
    R /= np.absolute(R)
    arr = R[R >= 0]
    r = np.array(arr.min())
    o = r.real
    p = float(o)
    q = round(p, 4)

    return q